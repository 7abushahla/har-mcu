"""One-shot orchestration for baseline, quantization, deployment exports, and TinyOL ablation."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import pandas as pd

from src.deploy.export_c_array import export_c_array
from src.deploy.export_norm_header import export_norm_header
from src.deploy.tflm_check_ops import DEFAULT_ALLOWED_OPS, get_model_ops
from src.eval.eval_baseline import evaluate_baseline_for_protocol
from src.eval.eval_tflite import evaluate_tflite
from src.quant.ptq_full_int8 import quantize_ptq_for_protocol
from src.quant.qat_train import qat_for_protocol
from src.sweeps.window_size_sweep import run_sweep_for_protocol
from src.tinyol.tinyol_sim import run_tinyol_sim
from src.train.train_baseline import train_baseline_for_protocol
from src.utils.artifacts import datacard_path, norm_stats_path, ptq_tflite_path
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


def _tflm_compatible(model_path: str) -> tuple[bool, list[str]]:
    ops = get_model_ops(model_path)
    unsupported = sorted([op for op in ops if op not in DEFAULT_ALLOWED_OPS])
    return len(unsupported) == 0, unsupported


def run_all(cfg: dict[str, Any], force_best_t: int | None = None) -> dict[str, Any]:
    ensure_path_dirs(cfg)
    reports_dir = Path(cfg["paths"]["reports_dir"])
    reports_dir.mkdir(parents=True, exist_ok=True)

    # 1) Sweep both protocols.
    for protocol in cfg.get("split_protocols", ["random_stratified"]):
        run_sweep_for_protocol(cfg, protocol)

    best_t = int(force_best_t if force_best_t is not None else _choose_best_window(cfg, "random_stratified"))
    cfg = dict(cfg)
    cfg["window_size_default"] = best_t

    final_rows: list[dict[str, Any]] = []

    for protocol in cfg.get("split_protocols", ["random_stratified"]):
        train_baseline_for_protocol(cfg, best_t, protocol)
        baseline_out = evaluate_baseline_for_protocol(cfg, best_t, protocol)

        ptq_out = quantize_ptq_for_protocol(cfg, best_t, protocol)
        ptq_eval = evaluate_tflite(cfg, ptq_out["tflite_model"], best_t, protocol, tag="ptq")

        qat_eval_acc = None
        qat_model_path = None
        if bool(cfg.get("quant", {}).get("qat", {}).get("enabled", True)):
            qat_out = qat_for_protocol(cfg, best_t, protocol)
            qat_model_path = qat_out["tflite"]
            try:
                qat_eval = evaluate_tflite(cfg, qat_model_path, best_t, protocol, tag="qat")
                qat_eval_acc = float(qat_eval["accuracy"])
            except Exception:
                qat_eval_acc = None

        ptq_size_kb = Path(ptq_out["tflite_model"]).stat().st_size / 1024.0

        model_out_dir = Path(cfg["paths"]["deploy_common_dir"]) / f"T{best_t}_P{protocol}"
        export_info = export_c_array(ptq_out["tflite_model"], str(model_out_dir), var_name="g_model_data")
        norm_json = norm_stats_path(cfg["paths"]["processed_dir"], best_t, protocol)
        export_norm_header(str(norm_json), str(model_out_dir / "norm_stats.h"))

        compatible, unsupported = _tflm_compatible(ptq_out["tflite_model"])

        baseline_metrics = _read_json(baseline_out["metrics_json"])
        ptq_metrics = _read_json(ptq_eval["metrics_json"])

        final_rows.append(
            {
                "protocol": protocol,
                "best_window_size": best_t,
                "baseline_accuracy": baseline_metrics["accuracy"],
                "baseline_macro_f1": baseline_metrics["macro_f1"],
                "ptq_accuracy": ptq_metrics["accuracy"],
                "ptq_macro_f1": ptq_metrics["macro_f1"],
                "qat_accuracy": qat_eval_acc,
                "model_size_kb_tflite": round(ptq_size_kb, 3),
                "tflm_compatible": compatible,
                "tflm_unsupported_ops": ";".join(unsupported),
                "deploy_model_header": export_info["header"],
                "deploy_model_source": export_info["source"],
                "arduino_flash_kb": None,
                "arduino_ram_arena_kb": cfg["deploy"]["tensor_arena_kb"],
                "invoke_ms": None,
                "end_to_end_latency_ms": None,
                "power_mw": None,
                "energy_per_inference_mj": None,
                "qat_tflite_model": qat_model_path,
            }
        )

    # TinyOL simulation on primary protocol at best T.
    primary_protocol = "random_stratified"
    tinyol_out = run_tinyol_sim(cfg, best_t, primary_protocol, k_labels=100, online_lr=0.01)

    table_path = reports_dir / "final_results_table.csv"
    if final_rows:
        with table_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(final_rows[0].keys()))
            writer.writeheader()
            writer.writerows(final_rows)

    summary_path = reports_dir / "run_all_summary.md"
    with summary_path.open("w", encoding="utf-8") as f:
        f.write("# Run-All Summary\n\n")
        f.write(f"- Best window size (primary protocol): {best_t}\n")
        f.write(f"- Final table: `{table_path}`\n")
        f.write(f"- TinyOL report: `{tinyol_out['report_md']}`\n")

    return {
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


if __name__ == "__main__":
    main()
