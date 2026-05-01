"""Fixed-schema Milestone 3 reporting helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from src.m3.config import M3_MASTER_COLUMNS
from src.utils.markdown_tables import dataframe_to_pipe_markdown


def _get(cfg: dict[str, Any], dotted: str, default: Any = None) -> Any:
    cur: Any = cfg
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur


def _nullable_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _inference_norm_applied(cfg: dict[str, Any]) -> bool:
    norm_mode = str(_get(cfg, "normalization.mode", "train_zscore"))
    if norm_mode == "none":
        return False
    return not bool(_get(cfg, "normalization.diagnostic_skip_inference_norm", False))


def _notes(cfg: dict[str, Any], row: dict[str, Any]) -> str:
    parts: list[str] = []
    run_id = row.get("run_id") or _get(cfg, "experiment.run_id")
    if run_id:
        parts.append(f"run_id={run_id}")
    if row.get("fp32_tflite_status"):
        parts.append(f"fp32_tflite={row['fp32_tflite_status']}")
    if row.get("ptq_status"):
        parts.append(f"ptq={row['ptq_status']}")
    if row.get("qat_status"):
        parts.append(f"qat={row['qat_status']}")
    transfer_notes = row.get("transfer_notes")
    if transfer_notes:
        parts.append(str(transfer_notes))
    cfg_notes = _get(cfg, "experiment.paper_targets.notes") or _get(
        cfg, "experiment.notes_assumptions"
    )
    if cfg_notes:
        parts.append(str(cfg_notes))
    return "; ".join(parts)


def m3_row_from_run(cfg: dict[str, Any], row: dict[str, Any]) -> dict[str, Any]:
    """Map a paper/transfer run row into the required M3 master schema."""

    ptq_status = row.get("ptq_status")
    qat_status = row.get("qat_status")
    deploy_gate_status = f"ptq={ptq_status or 'unknown'};qat={qat_status or 'skipped'}"
    target_sample_rate = float(_get(cfg, "data.target_sample_rate_hz", 20))
    window_size = int(row.get("window_size") or cfg.get("window_size_default"))

    mapped = {
        "experiment_id": str(_get(cfg, "m3.experiment_id")),
        "model_variant": str(_get(cfg, "experiment.model_variant")),
        "data_source": str(_get(cfg, "data.source")),
        "train_domain": str(_get(cfg, "data.train_domain")),
        "eval_domain": str(_get(cfg, "data.eval_domain")),
        "sample_rate_hz": float(_get(cfg, "data.sample_rate_hz", target_sample_rate)),
        "target_sample_rate_hz": target_sample_rate,
        "downsample": bool(_get(cfg, "data.downsample", False)),
        "window_size_samples": window_size,
        "window_duration_seconds": float(window_size) / target_sample_rate,
        "overlap": float(cfg.get("overlap", 0.5)),
        "unit_mode": str(_get(cfg, "data.unit_mode")),
        "normalization_mode": str(_get(cfg, "normalization.mode")),
        "inference_norm_applied": _inference_norm_applied(cfg),
        "split_protocol": str(row.get("protocol") or cfg.get("split_protocols", [""])[0]),
        "transfer_mode": str(_get(cfg, "m3.transfer_mode")),
        "seed": int(cfg.get("seed", 42)),
        "fp32_accuracy": _nullable_float(row.get("accuracy")),
        "fp32_macro_f1": _nullable_float(row.get("macro_f1")),
        "ptq_accuracy": _nullable_float(row.get("ptq_accuracy")),
        "ptq_macro_f1": _nullable_float(row.get("ptq_macro_f1")),
        "qat_accuracy": _nullable_float(row.get("qat_accuracy")),
        "qat_macro_f1": _nullable_float(row.get("qat_macro_f1")),
        "model_size_kb": _nullable_float(row.get("model_size_kb")),
        "latency_mean_ms": _nullable_float(row.get("ptq_inference_latency_ms_mean")),
        "latency_median_ms": _nullable_float(row.get("ptq_inference_latency_ms_median")),
        "latency_p95_ms": _nullable_float(row.get("ptq_inference_latency_ms_p95")),
        "deploy_gate_status": deploy_gate_status,
        "notes": _notes(cfg, row),
    }
    return {col: mapped.get(col) for col in M3_MASTER_COLUMNS}


def append_m3_results(
    reports_dir: str | Path,
    cfg: dict[str, Any],
    rows: list[dict[str, Any]],
) -> dict[str, str]:
    """Append fixed-schema rows to M3 master CSV/Markdown."""

    reports_path = Path(reports_dir)
    reports_path.mkdir(parents=True, exist_ok=True)
    csv_path = reports_path / "m3_experiment_master.csv"
    md_path = reports_path / "m3_experiment_master.md"

    incoming = pd.DataFrame([m3_row_from_run(cfg, row) for row in rows], columns=M3_MASTER_COLUMNS)
    if csv_path.exists():
        existing = pd.read_csv(csv_path)
        for col in M3_MASTER_COLUMNS:
            if col not in existing.columns:
                existing[col] = None
        merged = pd.concat([existing[M3_MASTER_COLUMNS], incoming], ignore_index=True)
        dedup_cols = [
            "experiment_id",
            "model_variant",
            "split_protocol",
            "transfer_mode",
            "seed",
        ]
        merged = merged.drop_duplicates(subset=dedup_cols, keep="last")
    else:
        merged = incoming

    merged.to_csv(csv_path, index=False)
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# M3 Experiment Master\n\n")
        f.write(f"- Total rows: `{len(merged)}`\n\n")
        if not merged.empty:
            f.write(dataframe_to_pipe_markdown(merged[M3_MASTER_COLUMNS]))
            f.write("\n")

    return {"csv": str(csv_path), "md": str(md_path)}
