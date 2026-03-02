"""Per-paper comparison table and chart exports."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd

from src.utils.artifacts import (
    paper_comparison_accuracy_png_path,
    paper_comparison_csv_path,
    paper_comparison_dir,
    paper_comparison_latency_png_path,
    paper_comparison_md_path,
    paper_comparison_size_png_path,
)


def _target_for_tier(paper_targets: dict[str, Any], tier: str) -> float | None:
    key_map = {"FP32": "fp32_accuracy", "PTQ INT8": "ptq_accuracy", "QAT INT8": "qat_accuracy"}
    key = key_map[tier]
    value = paper_targets.get(key)
    return float(value) if value is not None else None


def _delta_vs_target(value: float | None, target: float | None) -> float | None:
    if value is None or target is None:
        return None
    return float(value) - float(target)


def build_paper_comparison_rows(
    run_rows: list[dict[str, Any]],
    paper_targets: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    targets = paper_targets or {}
    out: list[dict[str, Any]] = []

    for row in run_rows:
        protocol = row.get("protocol")
        fp32_target = _target_for_tier(targets, "FP32")
        ptq_target = _target_for_tier(targets, "PTQ INT8")
        qat_target = _target_for_tier(targets, "QAT INT8")

        out.append(
            {
                "source": "wisdm_run",
                "protocol": protocol,
                "tier": "FP32",
                "accuracy": row.get("accuracy"),
                "macro_f1": row.get("macro_f1"),
                "model_size_kb": None,
                "training_time_sec": row.get("fp32_training_time_sec"),
                "inference_latency_ms_median": None,
                "inference_latency_ms_p95": None,
                "status": "ok",
                "paper_target_accuracy": fp32_target,
                "delta_vs_paper_accuracy": _delta_vs_target(row.get("accuracy"), fp32_target),
            }
        )
        out.append(
            {
                "source": "wisdm_run",
                "protocol": protocol,
                "tier": "PTQ INT8",
                "accuracy": row.get("ptq_accuracy"),
                "macro_f1": row.get("ptq_macro_f1"),
                "model_size_kb": row.get("ptq_model_size_kb"),
                "training_time_sec": None,
                "inference_latency_ms_median": row.get("ptq_inference_latency_ms_median"),
                "inference_latency_ms_p95": row.get("ptq_inference_latency_ms_p95"),
                "status": row.get("ptq_status"),
                "paper_target_accuracy": ptq_target,
                "delta_vs_paper_accuracy": _delta_vs_target(row.get("ptq_accuracy"), ptq_target),
            }
        )
        out.append(
            {
                "source": "wisdm_run",
                "protocol": protocol,
                "tier": "QAT INT8",
                "accuracy": row.get("qat_accuracy"),
                "macro_f1": row.get("qat_macro_f1"),
                "model_size_kb": row.get("qat_model_size_kb"),
                "training_time_sec": row.get("qat_training_time_sec"),
                "inference_latency_ms_median": row.get("qat_inference_latency_ms_median"),
                "inference_latency_ms_p95": row.get("qat_inference_latency_ms_p95"),
                "status": row.get("qat_status"),
                "paper_target_accuracy": qat_target,
                "delta_vs_paper_accuracy": _delta_vs_target(row.get("qat_accuracy"), qat_target),
            }
        )

    for tier in ("FP32", "PTQ INT8", "QAT INT8"):
        out.append(
            {
                "source": "paper_target",
                "protocol": "—",
                "tier": tier,
                "accuracy": _target_for_tier(targets, tier),
                "macro_f1": None,
                "model_size_kb": None,
                "training_time_sec": None,
                "inference_latency_ms_median": None,
                "inference_latency_ms_p95": None,
                "status": "reference",
                "paper_target_accuracy": _target_for_tier(targets, tier),
                "delta_vs_paper_accuracy": None,
            }
        )

    return out


def _plot_accuracy(df: pd.DataFrame, out_path: Path) -> None:
    rows = df[df["accuracy"].notna()].copy()
    fig, ax = plt.subplots(figsize=(max(10, len(rows) * 1.2), 5.5))
    if rows.empty:
        ax.text(0.5, 0.5, "No accuracy rows available", ha="center", va="center")
        ax.axis("off")
    else:
        labels = [f"{r.source}\n{r.protocol}\n{r.tier}" for r in rows.itertuples()]
        values = rows["accuracy"].astype(float).tolist()
        colors = [
            "#9e9e9e" if src == "paper_target" else ("#1f77b4" if tier == "FP32" else "#ff7f0e" if tier == "PTQ INT8" else "#2ca02c")
            for src, tier in zip(rows["source"], rows["tier"])
        ]
        bars = ax.bar(labels, values, color=colors, edgecolor="white")
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.002, f"{val:.4f}", ha="center", va="bottom", fontsize=8)
        ax.set_ylabel("Accuracy")
        ax.set_title("FP32/PTQ/QAT Accuracy Comparison")
        ax.grid(axis="y", alpha=0.3)
        ax.set_ylim(max(0.0, min(values) - 0.05), 1.02)
        plt.xticks(fontsize=8)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def _plot_model_size(df: pd.DataFrame, out_path: Path) -> None:
    rows = df[(df["tier"].isin(["PTQ INT8", "QAT INT8"])) & (df["model_size_kb"].notna()) & (df["source"] == "wisdm_run")].copy()
    fig, ax = plt.subplots(figsize=(max(8, len(rows) * 1.1), 4.8))
    if rows.empty:
        ax.text(0.5, 0.5, "No model-size rows available", ha="center", va="center")
        ax.axis("off")
    else:
        labels = [f"{r.protocol}\n{r.tier}" for r in rows.itertuples()]
        values = rows["model_size_kb"].astype(float).tolist()
        bars = ax.bar(labels, values, color="#4c78a8", edgecolor="white")
        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2, f"{val:.2f}", ha="center", va="bottom", fontsize=8)
        ax.set_ylabel("Model size (KB)")
        ax.set_title("Quantized Model Size (PTQ/QAT)")
        ax.grid(axis="y", alpha=0.3)
        plt.xticks(fontsize=8)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def _plot_latency(df: pd.DataFrame, out_path: Path) -> None:
    rows = df[
        (df["tier"].isin(["PTQ INT8", "QAT INT8"]))
        & (df["source"] == "wisdm_run")
        & (df["inference_latency_ms_median"].notna())
    ].copy()
    fig, ax = plt.subplots(figsize=(max(8, len(rows) * 1.2), 5.0))
    if rows.empty:
        ax.text(0.5, 0.5, "No latency rows available", ha="center", va="center")
        ax.axis("off")
    else:
        labels = [f"{r.protocol}\n{r.tier}" for r in rows.itertuples()]
        x = list(range(len(labels)))
        med = rows["inference_latency_ms_median"].astype(float).tolist()
        p95 = rows["inference_latency_ms_p95"].astype(float).tolist()
        width = 0.38
        ax.bar([i - width / 2 for i in x], med, width=width, label="median (ms)", color="#59a14f")
        ax.bar([i + width / 2 for i in x], p95, width=width, label="p95 (ms)", color="#e15759")
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=8)
        ax.set_ylabel("Latency (ms/sample)")
        ax.set_title("TFLite Inference Latency (Median + p95)")
        ax.grid(axis="y", alpha=0.3)
        ax.legend()
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)


def export_paper_comparison(
    reports_dir: str | Path,
    paper_slug: str,
    run_rows: list[dict[str, Any]],
    *,
    paper_targets: dict[str, Any] | None = None,
) -> dict[str, str]:
    out_dir = paper_comparison_dir(reports_dir, paper_slug)
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = build_paper_comparison_rows(run_rows, paper_targets=paper_targets)
    df = pd.DataFrame(rows)

    csv_path = paper_comparison_csv_path(reports_dir, paper_slug)
    md_path = paper_comparison_md_path(reports_dir, paper_slug)
    accuracy_png = paper_comparison_accuracy_png_path(reports_dir, paper_slug)
    size_png = paper_comparison_size_png_path(reports_dir, paper_slug)
    latency_png = paper_comparison_latency_png_path(reports_dir, paper_slug)

    df.to_csv(csv_path, index=False)
    with md_path.open("w", encoding="utf-8") as f:
        f.write(f"# {paper_slug} Comparison\n\n")
        notes = (paper_targets or {}).get("notes")
        if notes:
            f.write(f"- Notes: {notes}\n\n")
        keep_cols = [
            "source",
            "protocol",
            "tier",
            "accuracy",
            "macro_f1",
            "model_size_kb",
            "training_time_sec",
            "inference_latency_ms_median",
            "inference_latency_ms_p95",
            "paper_target_accuracy",
            "delta_vs_paper_accuracy",
            "status",
        ]
        f.write(df[keep_cols].to_markdown(index=False))
        f.write("\n")

    _plot_accuracy(df, accuracy_png)
    _plot_model_size(df, size_png)
    _plot_latency(df, latency_png)

    return {
        "csv": str(csv_path),
        "md": str(md_path),
        "accuracy_png": str(accuracy_png),
        "size_png": str(size_png),
        "latency_png": str(latency_png),
    }
