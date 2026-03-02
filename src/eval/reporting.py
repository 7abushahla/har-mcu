"""Paper-level and master result reporting helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
from src.utils.markdown_tables import dataframe_to_pipe_markdown


def export_paper_results(
    reports_dir: str | Path,
    paper_slug: str,
    protocol: str,
    rows: list[dict[str, Any]],
) -> dict[str, str]:
    out_dir = Path(reports_dir) / paper_slug
    out_dir.mkdir(parents=True, exist_ok=True)

    csv_path = out_dir / f"{paper_slug}_results_{protocol}.csv"
    md_path = out_dir / f"{paper_slug}_summary.md"

    df = pd.DataFrame(rows)
    df.to_csv(csv_path, index=False)

    with md_path.open("w", encoding="utf-8") as f:
        f.write(f"# {paper_slug} Summary\n\n")
        f.write(f"- Protocol: `{protocol}`\n")
        f.write(f"- Rows: `{len(df)}`\n\n")
        if not df.empty:
            keep_cols = [
                c
                for c in [
                    "paper_slug",
                    "protocol",
                    "variant",
                    "run_mode",
                    "accuracy",
                    "macro_f1",
                    "ptq_status",
                    "qat_status",
                    "train_device",
                    "eval_fp32_device",
                    "ptq_device",
                    "eval_ptq_device",
                    "qat_device",
                    "eval_qat_device",
                    "fp32_training_time_sec",
                    "qat_training_time_sec",
                    "ptq_inference_latency_ms_median",
                    "ptq_inference_latency_ms_p95",
                    "qat_inference_latency_ms_median",
                    "qat_inference_latency_ms_p95",
                    "ptq_model_size_kb",
                    "qat_model_size_kb",
                    "model_size_kb",
                    "paper_target_score",
                    "delta_vs_paper",
                ]
                if c in df.columns
            ]
            if keep_cols:
                f.write(dataframe_to_pipe_markdown(df[keep_cols]))
                f.write("\n")

    return {"csv": str(csv_path), "md": str(md_path)}


def append_master_results(
    reports_dir: str | Path,
    rows: list[dict[str, Any]],
) -> dict[str, str]:
    reports_dir = Path(reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)

    master_csv = reports_dir / "results_master.csv"
    master_md = reports_dir / "results_master.md"

    incoming = pd.DataFrame(rows)
    if master_csv.exists():
        existing = pd.read_csv(master_csv)
        merged = pd.concat([existing, incoming], ignore_index=True)
        dedup_cols = [c for c in ["paper_slug", "protocol", "variant", "run_id"] if c in merged.columns]
        if dedup_cols:
            merged = merged.drop_duplicates(subset=dedup_cols, keep="last")
    else:
        merged = incoming

    merged.to_csv(master_csv, index=False)
    with master_md.open("w", encoding="utf-8") as f:
        f.write("# Master Results\n\n")
        f.write(f"- Total rows: `{len(merged)}`\n\n")
        if not merged.empty:
            keep_cols = [
                c
                for c in [
                    "paper_slug",
                    "protocol",
                    "variant",
                    "run_id",
                    "run_mode",
                    "compression_focus",
                    "accuracy",
                    "macro_f1",
                    "train_device",
                    "eval_fp32_device",
                    "ptq_device",
                    "eval_ptq_device",
                    "qat_device",
                    "eval_qat_device",
                    "fp32_training_time_sec",
                    "qat_training_time_sec",
                    "ptq_inference_latency_ms_median",
                    "ptq_inference_latency_ms_p95",
                    "qat_inference_latency_ms_median",
                    "qat_inference_latency_ms_p95",
                    "ptq_model_size_kb",
                    "qat_model_size_kb",
                    "paper_target_score",
                    "delta_vs_paper",
                    "notes_assumptions",
                ]
                if c in merged.columns
            ]
            if keep_cols:
                f.write(dataframe_to_pipe_markdown(merged[keep_cols]))
                f.write("\n")

    return {"csv": str(master_csv), "md": str(master_md)}
