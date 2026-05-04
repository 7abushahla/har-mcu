"""Training-time accelerometer augmentation helpers."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import tensorflow as tf

from src.utils.artifacts import norm_stats_path


@dataclass(frozen=True)
class AccelRotationSettings:
    enabled: bool
    probability: float
    apply_in_qat: bool
    mode: str


@dataclass(frozen=True)
class TrainingInput:
    """Arguments for a Keras fit call.

    When augmentation is disabled, ``x`` and ``y`` are normal arrays and
    ``fit_kwargs`` contains the requested batch size. When augmentation is
    enabled, ``x`` is a Sequence that already batches ``(X, y)`` pairs.
    """

    x: Any
    y: np.ndarray | None
    fit_kwargs: dict[str, Any]
    augmentation_enabled: bool

    def fit_args(self) -> tuple[Any, ...]:
        if self.y is None:
            return (self.x,)
        return (self.x, self.y)


def accel_rotation_settings(cfg: dict[str, Any], *, for_qat: bool = False) -> AccelRotationSettings:
    rotation_cfg = cfg.get("augment", {}).get("accel_rotation", {})
    enabled = bool(rotation_cfg.get("enabled", False))
    apply_in_qat = bool(rotation_cfg.get("apply_in_qat", True))
    probability = float(rotation_cfg.get("probability", 0.0))
    mode = str(rotation_cfg.get("mode", "uniform_so3")).strip().lower()

    if for_qat and not apply_in_qat:
        enabled = False
    if probability <= 0.0:
        enabled = False

    if enabled:
        if mode != "uniform_so3":
            raise ValueError(f"Unsupported accelerometer rotation mode: {mode!r}")
        if probability > 1.0:
            raise ValueError("augment.accel_rotation.probability must be in [0, 1]")

    return AccelRotationSettings(
        enabled=enabled,
        probability=min(max(probability, 0.0), 1.0),
        apply_in_qat=apply_in_qat,
        mode=mode,
    )


def load_train_axis_stats(
    processed_dir: str | Path,
    window_size: int,
    protocol: str,
) -> tuple[np.ndarray, np.ndarray]:
    stats_file = norm_stats_path(processed_dir, window_size, protocol)
    with Path(stats_file).open("r", encoding="utf-8") as f:
        stats = json.load(f)

    mean = np.asarray(stats["mean"], dtype=np.float32).reshape(1, 1, -1)
    std = np.asarray(stats["std"], dtype=np.float32).reshape(1, 1, -1)
    if mean.shape[-1] != 3 or std.shape[-1] != 3:
        raise ValueError(
            f"Accelerometer rotation requires exactly 3 feature channels, got mean={mean.shape}, std={std.shape}"
        )
    return mean, std


def sample_uniform_so3(
    rng: np.random.Generator,
    count: int,
) -> np.ndarray:
    """Sample valid 3D rotation matrices uniformly from SO(3)."""

    if count < 0:
        raise ValueError("count must be non-negative")
    if count == 0:
        return np.empty((0, 3, 3), dtype=np.float32)

    u1 = rng.random(count, dtype=np.float32)
    u2 = rng.random(count, dtype=np.float32)
    u3 = rng.random(count, dtype=np.float32)
    two_pi = np.float32(2.0 * np.pi)

    qx = np.sqrt(1.0 - u1) * np.sin(two_pi * u2)
    qy = np.sqrt(1.0 - u1) * np.cos(two_pi * u2)
    qz = np.sqrt(u1) * np.sin(two_pi * u3)
    qw = np.sqrt(u1) * np.cos(two_pi * u3)

    xx = qx * qx
    yy = qy * qy
    zz = qz * qz
    xy = qx * qy
    xz = qx * qz
    yz = qy * qz
    xw = qx * qw
    yw = qy * qw
    zw = qz * qw

    rotations = np.empty((count, 3, 3), dtype=np.float32)
    rotations[:, 0, 0] = 1.0 - 2.0 * (yy + zz)
    rotations[:, 0, 1] = 2.0 * (xy - zw)
    rotations[:, 0, 2] = 2.0 * (xz + yw)
    rotations[:, 1, 0] = 2.0 * (xy + zw)
    rotations[:, 1, 1] = 1.0 - 2.0 * (xx + zz)
    rotations[:, 1, 2] = 2.0 * (yz - xw)
    rotations[:, 2, 0] = 2.0 * (xz - yw)
    rotations[:, 2, 1] = 2.0 * (yz + xw)
    rotations[:, 2, 2] = 1.0 - 2.0 * (xx + yy)
    return rotations


def rotate_raw_windows(windows: np.ndarray, rotations: np.ndarray) -> np.ndarray:
    """Apply one 3D rotation matrix per ``[T, 3]`` window."""

    windows = np.asarray(windows, dtype=np.float32)
    rotations = np.asarray(rotations, dtype=np.float32)
    if windows.ndim != 3 or windows.shape[-1] != 3:
        raise ValueError(f"Expected windows shape [N,T,3], got {windows.shape}")
    if rotations.shape != (windows.shape[0], 3, 3):
        raise ValueError(
            f"Expected rotations shape ({windows.shape[0]}, 3, 3), got {rotations.shape}"
        )
    return np.einsum("ntc,ncd->ntd", windows, rotations).astype(np.float32)


def rotate_normalized_accel_windows(
    X_normalized: np.ndarray,
    *,
    mean: np.ndarray,
    std: np.ndarray,
    probability: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """Denormalize windows, rotate in raw accel units, then re-normalize."""

    if X_normalized.ndim != 3 or X_normalized.shape[-1] != 3:
        raise ValueError(f"Expected X shape [N,T,3], got {X_normalized.shape}")

    X_aug = np.asarray(X_normalized, dtype=np.float32).copy()
    if X_aug.shape[0] == 0 or probability <= 0.0:
        return X_aug

    mask = rng.random(X_aug.shape[0]) < probability
    if not np.any(mask):
        return X_aug

    raw = X_aug[mask] * std + mean
    rotations = sample_uniform_so3(rng, int(mask.sum()))
    raw_rotated = rotate_raw_windows(raw, rotations)
    X_aug[mask] = (raw_rotated - mean) / std
    return X_aug.astype(np.float32)


class AccelRotationSequence(tf.keras.utils.Sequence):
    """Keras Sequence that augments only training batches."""

    def __init__(
        self,
        X: np.ndarray,
        y: np.ndarray,
        *,
        batch_size: int,
        mean: np.ndarray,
        std: np.ndarray,
        probability: float,
        seed: int,
        shuffle: bool = True,
    ) -> None:
        if X.ndim != 3 or X.shape[-1] != 3:
            raise ValueError(f"Expected X shape [N,T,3], got {X.shape}")
        if len(X) != len(y):
            raise ValueError(f"X and y length mismatch: {len(X)} != {len(y)}")
        if batch_size <= 0:
            raise ValueError("batch_size must be positive")

        self.X = np.asarray(X, dtype=np.float32)
        self.y = np.asarray(y)
        self.batch_size = int(batch_size)
        self.mean = np.asarray(mean, dtype=np.float32)
        self.std = np.asarray(std, dtype=np.float32)
        self.probability = float(probability)
        self.shuffle = bool(shuffle)
        self.rng = np.random.default_rng(int(seed))
        self.indices = np.arange(len(self.X))
        self.on_epoch_end()

    def __len__(self) -> int:
        return int(np.ceil(len(self.X) / self.batch_size))

    def __getitem__(self, index: int) -> tuple[np.ndarray, np.ndarray]:
        start = index * self.batch_size
        stop = min(start + self.batch_size, len(self.indices))
        batch_idx = self.indices[start:stop]
        batch_x = rotate_normalized_accel_windows(
            self.X[batch_idx],
            mean=self.mean,
            std=self.std,
            probability=self.probability,
            rng=self.rng,
        )
        batch_y = self.y[batch_idx]
        return batch_x, batch_y

    def on_epoch_end(self) -> None:
        if self.shuffle:
            self.rng.shuffle(self.indices)


def build_training_input(
    cfg: dict[str, Any],
    X_train: np.ndarray,
    y_train: np.ndarray,
    *,
    processed_dir: str | Path,
    window_size: int,
    protocol: str,
    batch_size: int,
    for_qat: bool = False,
) -> TrainingInput:
    """Build the object passed to ``model.fit`` for train-only augmentation."""

    settings = accel_rotation_settings(cfg, for_qat=for_qat)
    if not settings.enabled:
        return TrainingInput(
            x=X_train,
            y=y_train,
            fit_kwargs={"batch_size": int(batch_size)},
            augmentation_enabled=False,
        )

    mean, std = load_train_axis_stats(processed_dir, window_size, protocol)
    sequence = AccelRotationSequence(
        X_train,
        y_train,
        batch_size=int(batch_size),
        mean=mean,
        std=std,
        probability=settings.probability,
        seed=int(cfg.get("seed", 42)),
        shuffle=True,
    )
    return TrainingInput(
        x=sequence,
        y=None,
        fit_kwargs={},
        augmentation_enabled=True,
    )
