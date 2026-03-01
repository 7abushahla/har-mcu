"""One-shot orchestration for baseline, quantization, deployment exports, and TinyOL ablation."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import pandas as pd

from src.deploy.export_c_array import export_c_array
from src.deploy.export_norm_header import export_norm_header
from src.eval.eval_baseline import evaluate_baseline_for_protocol
from src.eval.eval_tflite import evaluate_tflite
from src.quant.ptq_full_int8 import quantize_ptq_for_protocol
from src.quant.qat_train import qat_for_protocol
from src.sweeps.window_size_sweep import run_sweep_for_protocol
from src.tinyol.tinyol_sim import run_tinyol_sim
from src.train.train_baseline import train_baseline_for_protocol
from src.utils.artifacts import norm_stats_path
from src.utils.config import apply_common_overrides, build_parser, ensure_path_dirs, load_yaml


def _choose_best_window(cfg: dict[str, Any], protocol: str = "random_stratified") -> int:
    sweep_csv = Path(cfg["paths"]["reports_dir"]) / f"window_sweep_P{protocol}.csv"
    if not sweep_csv.exists():
        run_sweep_for_protocol(cfg, protocol)

    df = pd.read_csv(sweep_csv)
    row = df.sort_values("accuracy", ascending=False).iloc[0]
    return int(row["window_size"])


def _read_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def _strict_ok(payload: dict[str, Any]) -> bool:
    return bool(
        payload.get("status") == "ok"
        and payload.get("deployable_full_int8", False)
        and payload.get("tflm_compatible", False)
    )


def _report_path(reports_dir: str | Path, kind: str, window_size: int, protocol: str) -> Path:
    return Path(reports_dir) / f"{kind}_export_T{window_size}_P{protocol}.json"


def run_all(cfg: dict[str, Any], force_best_t: int | None = None) -> dict[str, Any]:
    ensure_path_dirs(cfg)
    reports_dir = Path(cfg["paths"]["reports_dir"])
    reports_dir.mkdir(parents=True, exist_ok=True)

    for protocol in cfg.get("split_protocols", ["random_stratified"]):
        run_sweep_for_protocol(cfg, protocol)

    best_t = int(
        force_best_t if force_best_t is not None else _choose_best_window(cfg, "random_stratified")
    )
    cfg = dict(cfg)
    cfg["window_size_default"] = best_t

    final_rows: list[dict[str, Any]] = []

    for protocol in cfg.get("split_protocols", ["random_stratified"]):
        train_baseline_for_protocol(cfg, best_t, protocol)
        baseline_out = evaluate_baseline_for_protocol(cfg, best_t, protocol)
        baseline_metrics = _read_json(baseline_out["metrics_json"])

        row: dict[str, Any] = {
            "protocol": protocol,
            "best_window_size": best_t,
            "baseline_accuracy": baseline_metrics["accuracy"],
            "baseline_macro_f1": baseline_metrics["macro_f1"],
            "ptq_accuracy": None,
            "ptq_macro_f1": None,
            "qat_accuracy": None,
            "qat_macro_f1": None,
            "model_size_kb_tflite": None,
            "ptq_tflm_compatible": False,
            "ptq_unsupported_ops": "",
            "ptq_status": "failed",
            "ptq_error": None,
            "qat_tflm_compatible": False,
            "qat_unsupported_ops": "",
            "qat_status": "failed",
            "qat_error": None,
            "deploy_model_header": None,
            "deploy_model_source": None,
            "arduino_flash_kb": None,
            "arduino_ram_arena_kb": cfg["deploy"]["tensor_arena_kb"],
            "invoke_ms": None,
            "end_to_end_latency_ms": None,
            "power_mw": None,
            "energy_per_inference_mj": None,
            "ptq_tflite_model": None,
            "qat_tflite_model": None,
            "status": "ok",
            "error": None,
        }

        errors: list[str] = []
        ptq_ok = False
        qat_ok = not bool(cfg.get("quant", {}).get("qat", {}).get("enabled", True))

        ptq_export: dict[str, Any] = {}
        ptq_exc: str | None = None
        try:
            ptq_out = quantize_ptq_for_protocol(cfg, best_t, protocol)
            row["ptq_tflite_model"] = ptq_out["tflite_model"]
            ptq_export = _read_json(ptq_out["report_json"])
        except Exception as exc:
            ptq_exc = str(exc)
            fallback_report = _report_path(cfg["paths"]["reports_dir"], "ptq", best_t, protocol)
            if fallback_report.exists():
                ptq_export = _read_json(fallback_report)

        if ptq_export:
            row["ptq_status"] = str(ptq_export.get("status", "failed"))
            row["ptq_error"] = ptq_export.get("error")
            row["ptq_tflm_compatible"] = bool(ptq_export.get("tflm_compatible", False))
            row["ptq_unsupported_ops"] = ";".join(ptq_export.get("unsupported_ops", []))
            row["ptq_tflite_model"] = ptq_export.get("tflite_model", row["ptq_tflite_model"])
            ptq_ok = _strict_ok(ptq_export)
        else:
            row["ptq_error"] = ptq_exc or "PTQ report missing"

        if ptq_ok and row["ptq_tflite_model"]:
            ptq_eval = evaluate_tflite(cfg, row["ptq_tflite_model"], best_t, protocol, tag="ptq")
            ptq_metrics = _read_json(ptq_eval["metrics_json"])
            row["ptq_accuracy"] = float(ptq_metrics["accuracy"])
            row["ptq_macro_f1"] = float(ptq_metrics["macro_f1"])
            row["model_size_kb_tflite"] = round(float(ptq_metrics["model_size_kb"]), 3)

            model_out_dir = Path(cfg["paths"]["deploy_common_dir"]) / f"T{best_t}_P{protocol}"
            export_info = export_c_array(row["ptq_tflite_model"], str(model_out_dir), var_name="g_model_data")
            norm_json = norm_stats_path(cfg["paths"]["processed_dir"], best_t, protocol)
            export_norm_header(str(norm_json), str(model_out_dir / "norm_stats.h"))
            row["deploy_model_header"] = export_info["header"]
            row["deploy_model_source"] = export_info["source"]
        else:
            errors.append("PTQ strict gate failed")

        if bool(cfg.get("quant", {}).get("qat", {}).get("enabled", True)):
            qat_export: dict[str, Any] = {}
            qat_exc: str | None = None
            try:
                qat_out = qat_for_protocol(cfg, best_t, protocol)
                row["qat_tflite_model"] = qat_out["tflite"]
                qat_export = _read_json(qat_out["report_json"])
            except Exception as exc:
                qat_exc = str(exc)
                fallback_report = _report_path(cfg["paths"]["reports_dir"], "qat", best_t, protocol)
                if fallback_report.exists():
                    qat_export = _read_json(fallback_report)

            if qat_export:
                row["qat_status"] = str(qat_export.get("status", "failed"))
                row["qat_error"] = qat_export.get("error")
                row["qat_tflm_compatible"] = bool(qat_export.get("tflm_compatible", False))
                row["qat_unsupported_ops"] = ";".join(qat_export.get("unsupported_ops", []))
                row["qat_tflite_model"] = qat_export.get("qat_tflite", row["qat_tflite_model"])
                qat_ok = _strict_ok(qat_export)
            else:
                row["qat_error"] = qat_exc or "QAT report missing"
                qat_ok = False

            if qat_ok and row["qat_tflite_model"]:
                qat_eval = evaluate_tflite(cfg, row["qat_tflite_model"], best_t, protocol, tag="qat")
                qat_metrics = _read_json(qat_eval["metrics_json"])
                row["qat_accuracy"] = float(qat_metrics["accuracy"])
                row["qat_macro_f1"] = float(qat_metrics["macro_f1"])
            else:
                errors.append("QAT strict gate failed")

        if errors:
            if not ptq_ok and not qat_ok and bool(cfg.get("quant", {}).get("qat", {}).get("enabled", True)):
                row["status"] = "ptq_qat_failed"
            elif not ptq_ok:
                row["status"] = "ptq_failed"
            elif not qat_ok:
                row["status"] = "qat_failed"
            row["error"] = " | ".join(
                [e for e in [row.get("ptq_error"), row.get("qat_error")] if e]
            ) or " | ".join(errors)

        final_rows.append(row)

    primary_protocol = "random_stratified"
    tinyol_out = run_tinyol_sim(cfg, best_t, primary_protocol, k_labels=100, online_lr=0.01)

    table_path = reports_dir / "final_results_table.csv"
    if final_rows:
        with table_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(final_rows[0].keys()))
            writer.writeheader()
            writer.writerows(final_rows)

    summary_path = reports_dir / "run_all_summary.md"
    overall_ok = all(str(r.get("status")) == "ok" for r in final_rows) if final_rows else False
    with summary_path.open("w", encoding="utf-8") as f:
        f.write("# Run-All Summary\n\n")
        f.write(f"- Status: **{'ok' if overall_ok else 'failed'}**\n")
        f.write(f"- Best window size (primary protocol): {best_t}\n")
        f.write(f"- Final table: `{table_path}`\n")
        f.write(f"- TinyOL report: `{tinyol_out['report_md']}`\n")

    return {
        "status": "ok" if overall_ok else "failed",
        "best_window_size": best_t,
        "final_table": str(table_path),
        "summary_md": str(summary_path),
        "tinyol_report": tinyol_out["report_md"],
    }


def main() -> None:
    parser = build_parser("Run full HAR pipeline bundle")
    parser.add_argument("--best-t", type=int, default=None, help="Override best window size")
    args = parser.parse_args()

    cfg = apply_common_overrides(load_yaml(args.config), args)
    out = run_all(cfg, force_best_t=args.best_t)
    for k, v in out.items():
        print(f"{k}: {v}")

    raise SystemExit(0 if out["status"] == "ok" else 1)


if __name__ == "__main__":
    main()
