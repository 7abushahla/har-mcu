"""Normalization helpers (train-only stats)."""

from __future__ import annotations

import numpy as np


def fit_axis_stats(X_train: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    if X_train.ndim != 3 or X_train.shape[-1] != 3:
        raise ValueError(f"Expected X_train shape [N,T,3], got {X_train.shape}")

    mean = X_train.mean(axis=(0, 1), keepdims=True)
    std = X_train.std(axis=(0, 1), keepdims=True)
    std = np.where(std < 1e-8, 1.0, std)
    return mean.astype(np.float32), std.astype(np.float32)


def apply_axis_stats(X: np.ndarray, mean: np.ndarray, std: np.ndarray) -> np.ndarray:
    return ((X - mean) / std).astype(np.float32)
