from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from src.train.augment import (
    build_training_input,
    rotate_raw_windows,
    sample_uniform_so3,
)
from src.utils.artifacts import norm_stats_path


def _write_norm_stats(path: Path, mean: list[float], std: list[float]) -> None:
    path.write_text(
        json.dumps(
            {
                "axis_columns": ["x-axis", "y-axis", "z-axis"],
                "mean": mean,
                "std": std,
                "normalization_mode": "train_zscore",
            }
        ),
        encoding="utf-8",
    )


def test_uniform_so3_rotation_preserves_raw_vector_norms() -> None:
    rng = np.random.default_rng(123)
    raw = rng.normal(size=(12, 20, 3)).astype(np.float32)
    rotations = sample_uniform_so3(rng, raw.shape[0])

    rotated = rotate_raw_windows(raw, rotations)

    np.testing.assert_allclose(
        np.linalg.norm(rotated, axis=-1),
        np.linalg.norm(raw, axis=-1),
        rtol=1e-5,
        atol=1e-5,
    )
    np.testing.assert_allclose(
        np.linalg.det(rotations),
        np.ones(raw.shape[0], dtype=np.float32),
        rtol=1e-5,
        atol=1e-5,
    )


def test_training_input_builder_does_not_mutate_val_or_test_arrays(tmp_path: Path) -> None:
    rng = np.random.default_rng(456)
    mean = np.array([0.4, -0.2, 0.7], dtype=np.float32).reshape(1, 1, 3)
    std = np.array([1.5, 2.0, 0.5], dtype=np.float32).reshape(1, 1, 3)
    raw_train = rng.normal(size=(8, 6, 3)).astype(np.float32)
    X_train = ((raw_train - mean) / std).astype(np.float32)
    y_train = np.eye(3, dtype=np.float32)[np.arange(len(X_train)) % 3]

    X_val = rng.normal(size=(4, 6, 3)).astype(np.float32)
    X_test = rng.normal(size=(5, 6, 3)).astype(np.float32)
    X_train_before = X_train.copy()
    X_val_before = X_val.copy()
    X_test_before = X_test.copy()

    stats_path = norm_stats_path(tmp_path, 6, "random_stratified")
    _write_norm_stats(stats_path, mean.reshape(-1).tolist(), std.reshape(-1).tolist())
    cfg = {
        "seed": 99,
        "augment": {
            "accel_rotation": {
                "enabled": True,
                "probability": 1.0,
                "apply_in_qat": True,
                "mode": "uniform_so3",
            }
        },
    }

    train_input = build_training_input(
        cfg,
        X_train,
        y_train,
        processed_dir=tmp_path,
        window_size=6,
        protocol="random_stratified",
        batch_size=4,
    )
    assert train_input.augmentation_enabled is True
    _batch_x, _batch_y = train_input.x[0]

    np.testing.assert_array_equal(X_train, X_train_before)
    np.testing.assert_array_equal(X_val, X_val_before)
    np.testing.assert_array_equal(X_test, X_test_before)


def test_disabled_training_input_does_not_require_norm_stats(tmp_path: Path) -> None:
    X_train = np.zeros((3, 4, 3), dtype=np.float32)
    y_train = np.eye(2, dtype=np.float32)[[0, 1, 0]]
    cfg = {"augment": {"accel_rotation": {"enabled": False}}}

    train_input = build_training_input(
        cfg,
        X_train,
        y_train,
        processed_dir=tmp_path,
        window_size=4,
        protocol="random_stratified",
        batch_size=2,
    )

    assert train_input.augmentation_enabled is False
    assert train_input.x is X_train
    assert train_input.y is y_train
    assert train_input.fit_kwargs == {"batch_size": 2}
