"""Artifact naming and path helpers."""

from __future__ import annotations

from pathlib import Path


def slug_protocol(protocol: str) -> str:
    return protocol.replace("-", "_")


def dataset_prefix(window_size: int, protocol: str) -> str:
    return f"T{window_size}_P{slug_protocol(protocol)}"


def variant_suffix(variant: str | None) -> str:
    if not variant:
        return ""
    return f"_{variant}"


def model_slug(model_name: str) -> str:
    """Return a filesystem-safe model slug."""
    return str(model_name).strip().lower().replace(" ", "_").replace("-", "_")


def run_prefix(
    model_name: str,
    window_size: int,
    protocol: str,
    run_id: str | None = None,
) -> str:
    base = f"{model_slug(model_name)}_{dataset_prefix(window_size, protocol)}"
    if run_id:
        return f"{base}_{run_id}"
    return base


def split_npz_path(processed_dir: str | Path, window_size: int, protocol: str) -> Path:
    return Path(processed_dir) / f"splits_{dataset_prefix(window_size, protocol)}.npz"


def datacard_path(processed_dir: str | Path, window_size: int, protocol: str) -> Path:
    return Path(processed_dir) / f"datacard_{dataset_prefix(window_size, protocol)}.json"


def norm_stats_path(processed_dir: str | Path, window_size: int, protocol: str) -> Path:
    return Path(processed_dir) / f"norm_stats_{dataset_prefix(window_size, protocol)}.json"


def arrays_prefix(processed_dir: str | Path, window_size: int, protocol: str) -> Path:
    return Path(processed_dir) / dataset_prefix(window_size, protocol)


def baseline_ckpt_path(checkpoints_dir: str | Path, window_size: int, protocol: str) -> Path:
    return Path(checkpoints_dir) / f"deepconv_lstm_{dataset_prefix(window_size, protocol)}.keras"


def model_ckpt_path(
    checkpoints_dir: str | Path,
    model_name: str,
    window_size: int,
    protocol: str,
    run_id: str | None = None,
) -> Path:
    return Path(checkpoints_dir) / f"{run_prefix(model_name, window_size, protocol, run_id)}.keras"


def history_path(checkpoints_dir: str | Path, window_size: int, protocol: str) -> Path:
    return Path(checkpoints_dir) / f"history_{dataset_prefix(window_size, protocol)}.json"


def model_history_path(
    checkpoints_dir: str | Path,
    model_name: str,
    window_size: int,
    protocol: str,
    run_id: str | None = None,
) -> Path:
    return Path(checkpoints_dir) / f"history_{run_prefix(model_name, window_size, protocol, run_id)}.json"


def baseline_metrics_json(reports_dir: str | Path, window_size: int, protocol: str) -> Path:
    return Path(reports_dir) / f"baseline_{dataset_prefix(window_size, protocol)}.json"


def model_metrics_json(
    reports_dir: str | Path,
    model_name: str,
    window_size: int,
    protocol: str,
    run_id: str | None = None,
) -> Path:
    return Path(reports_dir) / f"{run_prefix(model_name, window_size, protocol, run_id)}.json"


def baseline_report_md(reports_dir: str | Path, window_size: int, protocol: str) -> Path:
    return Path(reports_dir) / f"baseline_{dataset_prefix(window_size, protocol)}.md"


def model_report_md(
    reports_dir: str | Path,
    model_name: str,
    window_size: int,
    protocol: str,
    run_id: str | None = None,
) -> Path:
    return Path(reports_dir) / f"{run_prefix(model_name, window_size, protocol, run_id)}.md"


def confusion_png(reports_dir: str | Path, window_size: int, protocol: str, suffix: str = "baseline") -> Path:
    return Path(reports_dir) / f"confusion_{suffix}_{dataset_prefix(window_size, protocol)}.png"


def model_confusion_png(
    reports_dir: str | Path,
    model_name: str,
    window_size: int,
    protocol: str,
    run_id: str | None = None,
) -> Path:
    return Path(reports_dir) / f"confusion_{run_prefix(model_name, window_size, protocol, run_id)}.png"


def tflite_confusion_png(
    reports_dir: str | Path,
    tag: str,
    window_size: int,
    protocol: str,
) -> Path:
    return Path(reports_dir) / f"confusion_{tag}_{dataset_prefix(window_size, protocol)}.png"


def model_training_curve_png(
    reports_dir: str | Path,
    model_name: str,
    window_size: int,
    protocol: str,
    run_id: str | None = None,
    tier: str = "fp32",
) -> Path:
    return (
        Path(reports_dir)
        / f"curve_{tier}_{run_prefix(model_name, window_size, protocol, run_id)}.png"
    )


def ptq_tflite_path(
    models_dir: str | Path,
    window_size: int,
    protocol: str,
    variant: str | None = None,
) -> Path:
    suffix = variant_suffix(variant)
    return Path(models_dir) / f"deepconv_lstm_{dataset_prefix(window_size, protocol)}_ptq_int8{suffix}.tflite"


def model_ptq_tflite_path(
    models_dir: str | Path,
    model_name: str,
    window_size: int,
    protocol: str,
    run_id: str | None = None,
    variant: str | None = None,
) -> Path:
    suffix = variant_suffix(variant)
    return (
        Path(models_dir)
        / f"{run_prefix(model_name, window_size, protocol, run_id)}_ptq_int8{suffix}.tflite"
    )


def qat_tflite_path(
    models_dir: str | Path,
    window_size: int,
    protocol: str,
    variant: str | None = None,
) -> Path:
    suffix = variant_suffix(variant)
    return Path(models_dir) / f"deepconv_lstm_{dataset_prefix(window_size, protocol)}_qat{suffix}.tflite"


def model_qat_tflite_path(
    models_dir: str | Path,
    model_name: str,
    window_size: int,
    protocol: str,
    run_id: str | None = None,
    variant: str | None = None,
) -> Path:
    suffix = variant_suffix(variant)
    return Path(models_dir) / f"{run_prefix(model_name, window_size, protocol, run_id)}_qat{suffix}.tflite"


def model_qat_history_path(
    checkpoints_dir: str | Path,
    model_name: str,
    window_size: int,
    protocol: str,
    run_id: str | None = None,
    variant: str | None = None,
) -> Path:
    suffix = variant_suffix(variant)
    return (
        Path(checkpoints_dir)
        / f"history_{run_prefix(model_name, window_size, protocol, run_id)}_qat{suffix}.json"
    )


def paper_comparison_dir(reports_dir: str | Path, paper_slug: str) -> Path:
    return Path(reports_dir) / paper_slug / "comparison"


def paper_comparison_csv_path(reports_dir: str | Path, paper_slug: str) -> Path:
    return paper_comparison_dir(reports_dir, paper_slug) / f"{paper_slug}_comparison.csv"


def paper_comparison_md_path(reports_dir: str | Path, paper_slug: str) -> Path:
    return paper_comparison_dir(reports_dir, paper_slug) / f"{paper_slug}_comparison.md"


def paper_comparison_accuracy_png_path(reports_dir: str | Path, paper_slug: str) -> Path:
    return paper_comparison_dir(reports_dir, paper_slug) / f"{paper_slug}_comparison_accuracy.png"


def paper_comparison_size_png_path(reports_dir: str | Path, paper_slug: str) -> Path:
    return paper_comparison_dir(reports_dir, paper_slug) / f"{paper_slug}_comparison_size.png"


def paper_comparison_latency_png_path(reports_dir: str | Path, paper_slug: str) -> Path:
    return paper_comparison_dir(reports_dir, paper_slug) / f"{paper_slug}_comparison_latency.png"
