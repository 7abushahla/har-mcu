"""Processed dataset I/O utilities."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from src.utils.artifacts import arrays_prefix


def dataset_array_path(
    processed_dir: str | Path,
    split_name: str,
    kind: str,
    window_size: int,
    protocol: str,
) -> Path:
    prefix = arrays_prefix(processed_dir, window_size, protocol)
    return prefix.parent / f"{kind}_{split_name}_{prefix.name}.npy"


def dataset_exists(processed_dir: str | Path, window_size: int, protocol: str) -> bool:
    required = [
        dataset_array_path(processed_dir, "train", "X", window_size, protocol),
        dataset_array_path(processed_dir, "train", "y", window_size, protocol),
        dataset_array_path(processed_dir, "val", "X", window_size, protocol),
        dataset_array_path(processed_dir, "val", "y", window_size, protocol),
        dataset_array_path(processed_dir, "test", "X", window_size, protocol),
        dataset_array_path(processed_dir, "test", "y", window_size, protocol),
    ]
    return all(p.exists() for p in required)


def load_split_arrays(processed_dir: str | Path, window_size: int, protocol: str) -> dict[str, np.ndarray]:
    out = {}
    for split_name in ("train", "val", "test"):
        out[f"X_{split_name}"] = np.load(
            dataset_array_path(processed_dir, split_name, "X", window_size, protocol)
        )
        out[f"y_{split_name}"] = np.load(
            dataset_array_path(processed_dir, split_name, "y", window_size, protocol)
        )
    return out
