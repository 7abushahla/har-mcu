"""Fast end-to-end smoke test for the full pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from src.data.build_dataset import build_dataset_for_protocol
from src.deploy.export_c_array import export_c_array
from src.deploy.export_norm_header import export_norm_header
from src.eval.eval_baseline import evaluate_baseline_for_protocol
from src.eval.eval_tflite import evaluate_tflite
from src.quant.ptq_full_int8 import quantize_ptq_for_protocol
from src.quant.qat_train import qat_for_protocol
from src.train.train_baseline import train_baseline_for_protocol
from src.utils.artifacts import norm_stats_path
from src.utils.config import apply_common_overrides, build_parser, ensure_path_dirs, load_yaml
from src.utils.repro import dump_json, load_json


def _strict_ok(payload: dict[str, Any]) -> bool:
    return bool(
        payload.get("status") == "ok"
        and payload.get("deployable_full_int8", False)
        and payload.get("tflm_compatible", False)
    )


def _report_path(reports_dir: str | Path, kind: str, window_size: int, protocol: str) -> Path:
    return Path(reports_dir) / f"{kind}_export_T{window_size}_P{protocol}.json"


def run_smoke(cfg: dict[str, Any]) -> dict[str, Any]:
    ensure_path_dirs(cfg)

    cfg = dict(cfg)
    cfg.setdefault("smoke", {})["enabled"] = True
    cfg["train"]["epochs"] = int(cfg.get("smoke", {}).get("quick_epochs", cfg["train"]["epochs"]))

    ws = int(cfg["window_size_default"])
    artifacts: list[str] = []
    protocol_results: list[dict[str, Any]] = []

    ok = True
    errors: list[str] = []

    for protocol in cfg.get("split_protocols", ["random_stratified"]):
        try:
            build_dataset_for_protocol(cfg, ws, protocol)
            train_baseline_for_protocol(cfg, ws, protocol)
            base_eval = evaluate_baseline_for_protocol(cfg, ws, protocol)

            ptq_out = None
            ptq_export = {}
            ptq_eval = None
            ptq_exc: str | None = None
            try:
                ptq_out = quantize_ptq_for_protocol(cfg, ws, protocol)
                ptq_export = load_json(ptq_out["report_json"])
            except Exception as exc:
                ptq_exc = str(exc)
                fallback = _report_path(cfg["paths"]["reports_dir"], "ptq", ws, protocol)
                if fallback.exists():
                    ptq_export = load_json(fallback)

            ptq_ok = bool(ptq_export) and _strict_ok(ptq_export)
            ptq_model_path = ptq_export.get("tflite_model") if ptq_export else None
            if ptq_ok and ptq_model_path:
                ptq_eval = evaluate_tflite(cfg, ptq_model_path, ws, protocol, tag="ptq_smoke")

            qat_out = None
            qat_export = {}
            qat_eval = None
            qat_exc: str | None = None
            try:
                qat_out = qat_for_protocol(cfg, ws, protocol)
                qat_export = load_json(qat_out["report_json"])
            except Exception as exc:
                qat_exc = str(exc)
                fallback = _report_path(cfg["paths"]["reports_dir"], "qat", ws, protocol)
                if fallback.exists():
                    qat_export = load_json(fallback)

            qat_ok = bool(qat_export) and _strict_ok(qat_export)
            qat_model_path = qat_export.get("qat_tflite") if qat_export else None
            if qat_ok and qat_model_path:
                qat_eval = evaluate_tflite(cfg, qat_model_path, ws, protocol, tag="qat_smoke")

            if ptq_ok and ptq_model_path:
                out_dir = Path(cfg["paths"]["deploy_common_dir"]) / "smoke"
                c_out = export_c_array(ptq_model_path, str(out_dir), var_name="g_model_data")
                norm_json = norm_stats_path(cfg["paths"]["processed_dir"], ws, protocol)
                norm_out = export_norm_header(str(norm_json), str(out_dir / "norm_stats.h"))
                artifacts.extend(
                    [
                        base_eval["report_md"],
                        ptq_model_path,
                        qat_model_path,
                        c_out["header"],
                        c_out["source"],
                        norm_out["norm_header"],
                    ]
                )

            protocol_results.append(
                {
                    "protocol": protocol,
                    "baseline_report": base_eval["report_md"],
                    "ptq_report": ptq_out["report_md"] if ptq_out else None,
                    "ptq_eval_report": ptq_eval["report_md"] if ptq_eval else None,
                    "ptq_status": ptq_export.get("status") if ptq_export else "failed",
                    "ptq_error": ptq_export.get("error") if ptq_export else (ptq_exc or "report missing"),
                    "ptq_tflm_ops": ptq_export.get("tflm_ops", []) if ptq_export else [],
                    "ptq_unsupported": ptq_export.get("unsupported_ops", []) if ptq_export else [],
                    "ptq_compat": bool(ptq_export.get("tflm_compatible", False)) if ptq_export else False,
                    "qat_report": qat_out["report_md"] if qat_out else None,
                    "qat_eval_report": qat_eval["report_md"] if qat_eval else None,
                    "qat_status": qat_export.get("status") if qat_export else "failed",
                    "qat_error": qat_export.get("error") if qat_export else (qat_exc or "report missing"),
                    "qat_tflm_ops": qat_export.get("tflm_ops", []) if qat_export else [],
                    "qat_unsupported": qat_export.get("unsupported_ops", []) if qat_export else [],
                    "qat_compat": bool(qat_export.get("tflm_compatible", False)) if qat_export else False,
                }
            )

            if not ptq_ok:
                ok = False
                errors.append(
                    "Protocol "
                    + protocol
                    + ": PTQ strict gate failed: "
                    + str(ptq_export.get("error") if ptq_export else (ptq_exc or "report missing"))
                )
            if not qat_ok:
                ok = False
                errors.append(
                    "Protocol "
                    + protocol
                    + ": QAT strict gate failed: "
                    + str(qat_export.get("error") if qat_export else (qat_exc or "report missing"))
                )
        except Exception as exc:
            ok = False
            errors.append(f"Protocol {protocol}: {exc}")

    payload = {
        "status": "ok" if ok else "failed",
        "window_size": ws,
        "protocols": protocol_results,
        "artifacts": artifacts,
        "errors": errors,
    }

    reports_dir = Path(cfg["paths"]["reports_dir"])
    reports_dir.mkdir(parents=True, exist_ok=True)
    json_path = reports_dir / "smoke_report.json"
    md_path = reports_dir / "smoke_report.md"

    dump_json(json_path, payload)

    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Smoke Report\n\n")
        f.write(f"- Status: **{payload['status']}**\n")
        f.write(f"- Window size: {ws}\n\n")
        for pr in protocol_results:
            f.write(f"## Protocol: {pr['protocol']}\n\n")
            f.write(f"- PTQ status: `{pr['ptq_status']}`\n")
            f.write(f"- PTQ error: `{pr['ptq_error']}`\n")
            f.write(f"- PTQ compatibility: `{pr['ptq_compat']}`\n")
            f.write(f"- PTQ unsupported ops: `{', '.join(pr['ptq_unsupported'])}`\n")
            f.write(f"- QAT status: `{pr['qat_status']}`\n")
            f.write(f"- QAT error: `{pr['qat_error']}`\n")
            f.write(f"- QAT compatibility: `{pr['qat_compat']}`\n")
            f.write(f"- QAT unsupported ops: `{', '.join(pr['qat_unsupported'])}`\n")
            f.write(f"- Baseline report: `{pr['baseline_report']}`\n")
            f.write(f"- PTQ report: `{pr['ptq_report']}`\n")
            f.write(f"- PTQ eval: `{pr['ptq_eval_report']}`\n")
            f.write(f"- QAT report: `{pr['qat_report']}`\n")
            f.write(f"- QAT eval: `{pr['qat_eval_report']}`\n\n")
        if errors:
            f.write("## Errors\n\n")
            for err in errors:
                f.write(f"- {err}\n")

    return {"json": str(json_path), "md": str(md_path), "status": payload["status"]}


def main() -> None:
    parser = build_parser("Run smoke test for full pipeline")
    args = parser.parse_args()
    cfg = apply_common_overrides(load_yaml(args.config), args)

    out = run_smoke(cfg)
    for k, v in out.items():
        print(f"{k}: {v}")

    raise SystemExit(0 if out["status"] == "ok" else 1)


if __name__ == "__main__":
    main()
