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


def history_path(checkpoints_dir: str | Path, window_size: int, protocol: str) -> Path:
    return Path(checkpoints_dir) / f"history_{dataset_prefix(window_size, protocol)}.json"


def baseline_metrics_json(reports_dir: str | Path, window_size: int, protocol: str) -> Path:
    return Path(reports_dir) / f"baseline_{dataset_prefix(window_size, protocol)}.json"


def baseline_report_md(reports_dir: str | Path, window_size: int, protocol: str) -> Path:
    return Path(reports_dir) / f"baseline_{dataset_prefix(window_size, protocol)}.md"


def confusion_png(reports_dir: str | Path, window_size: int, protocol: str, suffix: str = "baseline") -> Path:
    return Path(reports_dir) / f"confusion_{suffix}_{dataset_prefix(window_size, protocol)}.png"


def ptq_tflite_path(
    models_dir: str | Path,
    window_size: int,
    protocol: str,
    variant: str | None = None,
) -> Path:
    suffix = variant_suffix(variant)
    return Path(models_dir) / f"deepconv_lstm_{dataset_prefix(window_size, protocol)}_ptq_int8{suffix}.tflite"


def qat_tflite_path(
    models_dir: str | Path,
    window_size: int,
    protocol: str,
    variant: str | None = None,
) -> Path:
    suffix = variant_suffix(variant)
    return Path(models_dir) / f"deepconv_lstm_{dataset_prefix(window_size, protocol)}_qat{suffix}.tflite"
