"""Fast end-to-end smoke test for the full pipeline."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.deploy.export_c_array import export_c_array
from src.deploy.export_norm_header import export_norm_header
from src.deploy.tflm_check_ops import DEFAULT_ALLOWED_OPS, get_model_ops
from src.eval.eval_baseline import evaluate_baseline_for_protocol
from src.eval.eval_tflite import evaluate_tflite
from src.quant.ptq_full_int8 import quantize_ptq_for_protocol
from src.train.train_baseline import train_baseline_for_protocol
from src.data.build_dataset import build_dataset_for_protocol
from src.utils.artifacts import norm_stats_path
from src.utils.config import apply_common_overrides, build_parser, ensure_path_dirs, load_yaml


def _tflm_check(model_path: str) -> tuple[bool, list[str], list[str]]:
    ops = get_model_ops(model_path)
    unsupported = sorted([op for op in ops if op not in DEFAULT_ALLOWED_OPS])
    return len(unsupported) == 0, ops, unsupported


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
            ptq = quantize_ptq_for_protocol(cfg, ws, protocol)
            ptq_eval = evaluate_tflite(cfg, ptq["tflite_model"], ws, protocol, tag="ptq_smoke")

            out_dir = Path(cfg["paths"]["deploy_common_dir"]) / "smoke"
            c_out = export_c_array(ptq["tflite_model"], str(out_dir), var_name="g_model_data")
            norm_json = norm_stats_path(cfg["paths"]["processed_dir"], ws, protocol)
            norm_out = export_norm_header(str(norm_json), str(out_dir / "norm_stats.h"))

            compat, ops, unsupported = _tflm_check(ptq["tflite_model"])
            if not compat:
                ok = False
                errors.append(
                    f"Protocol {protocol}: unsupported TFLM ops: {', '.join(unsupported)}"
                )

            protocol_results.append(
                {
                    "protocol": protocol,
                    "baseline_report": base_eval["report_md"],
                    "ptq_report": ptq["report_md"],
                    "ptq_eval_report": ptq_eval["report_md"],
                    "tflm_ops": ops,
                    "tflm_unsupported": unsupported,
                    "compat": compat,
                }
            )
            artifacts.extend([base_eval["report_md"], ptq["tflite_model"], c_out["header"], c_out["source"], norm_out["norm_header"]])
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

    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Smoke Report\n\n")
        f.write(f"- Status: **{payload['status']}**\n")
        f.write(f"- Window size: {ws}\n\n")
        for pr in protocol_results:
            f.write(f"## Protocol: {pr['protocol']}\n\n")
            f.write(f"- Compatibility: `{pr['compat']}`\n")
            f.write(f"- Unsupported ops: `{', '.join(pr['tflm_unsupported'])}`\n")
            f.write(f"- Baseline report: `{pr['baseline_report']}`\n")
            f.write(f"- PTQ report: `{pr['ptq_report']}`\n")
            f.write(f"- PTQ eval: `{pr['ptq_eval_report']}`\n\n")
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
