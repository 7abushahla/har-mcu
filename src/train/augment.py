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
    max_angle_degrees: float | None = None
    target_vectors: tuple[tuple[float, float, float], ...] | None = None
    target_probabilities: tuple[float, ...] | None = None


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
    max_angle_degrees = rotation_cfg.get("max_angle_degrees")
    max_angle_degrees = None if max_angle_degrees is None else float(max_angle_degrees)
    target_vectors = _parse_target_vectors(rotation_cfg.get("target_vectors"))
    target_probabilities = _parse_target_probabilities(
        rotation_cfg.get("target_probabilities"),
        count=0 if target_vectors is None else len(target_vectors),
    )

    if for_qat and not apply_in_qat:
        enabled = False
    if probability <= 0.0:
        enabled = False

    if enabled:
        if mode not in {"uniform_so3", "bounded_so3", "target_gravity"}:
            raise ValueError(f"Unsupported accelerometer rotation mode: {mode!r}")
        if probability > 1.0:
            raise ValueError("augment.accel_rotation.probability must be in [0, 1]")
        if mode == "bounded_so3":
            if max_angle_degrees is None:
                raise ValueError(
                    "augment.accel_rotation.max_angle_degrees is required for bounded_so3"
                )
            if not 0.0 < max_angle_degrees <= 180.0:
                raise ValueError(
                    "augment.accel_rotation.max_angle_degrees must be in (0, 180]"
                )
        if mode == "target_gravity" and not target_vectors:
            raise ValueError(
                "augment.accel_rotation.target_vectors is required for target_gravity"
            )

    return AccelRotationSettings(
        enabled=enabled,
        probability=min(max(probability, 0.0), 1.0),
        apply_in_qat=apply_in_qat,
        mode=mode,
        max_angle_degrees=max_angle_degrees,
        target_vectors=target_vectors,
        target_probabilities=target_probabilities,
    )


def _parse_target_vectors(
    value: Any,
) -> tuple[tuple[float, float, float], ...] | None:
    if value is None:
        return None
    if isinstance(value, str):
        groups = [group.strip() for group in value.split(";") if group.strip()]
        value = [[float(part.strip()) for part in group.split(",")] for group in groups]
    arr = np.asarray(value, dtype=np.float32)
    if arr.ndim != 2 or arr.shape[1] != 3 or arr.shape[0] == 0:
        raise ValueError(
            "augment.accel_rotation.target_vectors must be a non-empty [N, 3] list"
        )
    norms = np.linalg.norm(arr, axis=1)
    if np.any(norms <= np.finfo(np.float32).eps):
        raise ValueError("augment.accel_rotation.target_vectors cannot contain zero vectors")
    arr = arr / norms[:, None]
    return tuple(tuple(float(x) for x in row) for row in arr)


def _parse_target_probabilities(
    value: Any,
    *,
    count: int,
) -> tuple[float, ...] | None:
    if value is None:
        return None
    if count <= 0:
        raise ValueError(
            "augment.accel_rotation.target_probabilities requires target_vectors"
        )
    if isinstance(value, str):
        value = [float(part.strip()) for part in value.split(",") if part.strip()]
    probs = np.asarray(value, dtype=np.float32)
    if probs.shape != (count,):
        raise ValueError(
            "augment.accel_rotation.target_probabilities length must match target_vectors"
        )
    if np.any(probs < 0.0):
        raise ValueError("augment.accel_rotation.target_probabilities cannot be negative")
    total = float(np.sum(probs))
    if total <= 0.0:
        raise ValueError("augment.accel_rotation.target_probabilities must sum to > 0")
    probs = probs / total
    return tuple(float(x) for x in probs)


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


def _axis_angle_to_matrices(axes: np.ndarray, angles: np.ndarray) -> np.ndarray:
    axes = np.asarray(axes, dtype=np.float32)
    angles = np.asarray(angles, dtype=np.float32)
    if axes.ndim != 2 or axes.shape[-1] != 3:
        raise ValueError(f"Expected axes shape [N,3], got {axes.shape}")
    if angles.shape != (axes.shape[0],):
        raise ValueError(f"Expected angles shape ({axes.shape[0]},), got {angles.shape}")

    x = axes[:, 0]
    y = axes[:, 1]
    z = axes[:, 2]
    c = np.cos(angles)
    s = np.sin(angles)
    one_minus_c = 1.0 - c

    rotations = np.empty((axes.shape[0], 3, 3), dtype=np.float32)
    rotations[:, 0, 0] = c + x * x * one_minus_c
    rotations[:, 0, 1] = x * y * one_minus_c - z * s
    rotations[:, 0, 2] = x * z * one_minus_c + y * s
    rotations[:, 1, 0] = y * x * one_minus_c + z * s
    rotations[:, 1, 1] = c + y * y * one_minus_c
    rotations[:, 1, 2] = y * z * one_minus_c - x * s
    rotations[:, 2, 0] = z * x * one_minus_c - y * s
    rotations[:, 2, 1] = z * y * one_minus_c + x * s
    rotations[:, 2, 2] = c + z * z * one_minus_c
    return rotations


def sample_bounded_so3(
    rng: np.random.Generator,
    count: int,
    *,
    max_angle_degrees: float,
) -> np.ndarray:
    """Sample random 3D rotations with angle bounded around identity."""

    if count < 0:
        raise ValueError("count must be non-negative")
    if not 0.0 < float(max_angle_degrees) <= 180.0:
        raise ValueError("max_angle_degrees must be in (0, 180]")
    if count == 0:
        return np.empty((0, 3, 3), dtype=np.float32)

    axes = rng.normal(size=(count, 3)).astype(np.float32)
    axis_norm = np.linalg.norm(axes, axis=1, keepdims=True)
    axes = axes / np.maximum(axis_norm, np.finfo(np.float32).eps)
    max_angle = np.float32(np.deg2rad(float(max_angle_degrees)))
    angles = rng.uniform(-max_angle, max_angle, size=count).astype(np.float32)
    return _axis_angle_to_matrices(axes, angles)


def rotation_matrices_between_vectors(
    source_vectors: np.ndarray,
    target_vectors: np.ndarray,
) -> np.ndarray:
    """Return row-vector rotation matrices that map each source direction to target."""

    source = np.asarray(source_vectors, dtype=np.float32)
    target = np.asarray(target_vectors, dtype=np.float32)
    if source.ndim != 2 or source.shape[-1] != 3:
        raise ValueError(f"Expected source_vectors shape [N,3], got {source.shape}")
    if target.shape != source.shape:
        raise ValueError(f"Expected target_vectors shape {source.shape}, got {target.shape}")

    count = source.shape[0]
    rotations = np.tile(np.eye(3, dtype=np.float32), (count, 1, 1))
    source_norm = np.linalg.norm(source, axis=1, keepdims=True)
    target_norm = np.linalg.norm(target, axis=1, keepdims=True)
    valid = (
        (source_norm[:, 0] > np.finfo(np.float32).eps)
        & (target_norm[:, 0] > np.finfo(np.float32).eps)
    )
    if not np.any(valid):
        return rotations

    s = source[valid] / source_norm[valid]
    t = target[valid] / target_norm[valid]
    dot = np.sum(s * t, axis=1)
    dot = np.clip(dot, -1.0, 1.0)

    same = dot > 1.0 - 1e-6
    opposite = dot < -1.0 + 1e-6
    general = ~(same | opposite)

    valid_indices = np.flatnonzero(valid)
    if np.any(general):
        sg = s[general]
        tg = t[general]
        axes = np.cross(sg, tg).astype(np.float32)
        axis_norm = np.linalg.norm(axes, axis=1, keepdims=True)
        axes = axes / np.maximum(axis_norm, np.finfo(np.float32).eps)
        angles = np.arccos(dot[general]).astype(np.float32)
        # _axis_angle_to_matrices returns column-vector matrices. Transpose so
        # row-vector windows multiplied by R map source to target.
        rotations[valid_indices[general]] = np.transpose(
            _axis_angle_to_matrices(axes, angles),
            (0, 2, 1),
        )

    if np.any(opposite):
        so = s[opposite]
        helper = np.tile(np.array([1.0, 0.0, 0.0], dtype=np.float32), (len(so), 1))
        use_y = np.abs(np.sum(so * helper, axis=1)) > 0.9
        helper[use_y] = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        axes = np.cross(so, helper).astype(np.float32)
        axes = axes / np.maximum(
            np.linalg.norm(axes, axis=1, keepdims=True),
            np.finfo(np.float32).eps,
        )
        angles = np.full(len(so), np.pi, dtype=np.float32)
        rotations[valid_indices[opposite]] = np.transpose(
            _axis_angle_to_matrices(axes, angles),
            (0, 2, 1),
        )

    return rotations.astype(np.float32)


def sample_target_gravity_rotations(
    rng: np.random.Generator,
    windows: np.ndarray,
    *,
    target_vectors: tuple[tuple[float, float, float], ...],
    target_probabilities: tuple[float, ...] | None = None,
) -> np.ndarray:
    """Rotate each window mean-gravity proxy toward one configured target vector."""

    windows = np.asarray(windows, dtype=np.float32)
    if windows.ndim != 3 or windows.shape[-1] != 3:
        raise ValueError(f"Expected windows shape [N,T,3], got {windows.shape}")
    targets = np.asarray(target_vectors, dtype=np.float32)
    if targets.ndim != 2 or targets.shape[1] != 3 or targets.shape[0] == 0:
        raise ValueError("target_vectors must be a non-empty [N,3] array")
    targets = targets / np.maximum(
        np.linalg.norm(targets, axis=1, keepdims=True),
        np.finfo(np.float32).eps,
    )
    probabilities = None
    if target_probabilities is not None:
        probabilities = np.asarray(target_probabilities, dtype=np.float32)
        probabilities = probabilities / np.sum(probabilities)
    chosen = rng.choice(targets.shape[0], size=windows.shape[0], p=probabilities)
    source = np.mean(windows, axis=1)
    target = targets[chosen]
    return rotation_matrices_between_vectors(source, target)


def sample_rotation_matrices(
    rng: np.random.Generator,
    count: int,
    settings: AccelRotationSettings,
    *,
    windows: np.ndarray | None = None,
) -> np.ndarray:
    if settings.mode == "uniform_so3":
        return sample_uniform_so3(rng, count)
    if settings.mode == "bounded_so3":
        if settings.max_angle_degrees is None:
            raise ValueError("bounded_so3 requires max_angle_degrees")
        return sample_bounded_so3(
            rng,
            count,
            max_angle_degrees=float(settings.max_angle_degrees),
        )
    if settings.mode == "target_gravity":
        if windows is None:
            raise ValueError("target_gravity requires raw windows")
        if settings.target_vectors is None:
            raise ValueError("target_gravity requires target_vectors")
        return sample_target_gravity_rotations(
            rng,
            windows,
            target_vectors=settings.target_vectors,
            target_probabilities=settings.target_probabilities,
        )
    raise ValueError(f"Unsupported accelerometer rotation mode: {settings.mode!r}")


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
    settings: AccelRotationSettings,
    rng: np.random.Generator,
) -> np.ndarray:
    """Denormalize windows, rotate in raw accel units, then re-normalize."""

    if X_normalized.ndim != 3 or X_normalized.shape[-1] != 3:
        raise ValueError(f"Expected X shape [N,T,3], got {X_normalized.shape}")

    X_aug = np.asarray(X_normalized, dtype=np.float32).copy()
    probability = settings.probability
    if X_aug.shape[0] == 0 or probability <= 0.0:
        return X_aug

    mask = rng.random(X_aug.shape[0]) < probability
    if not np.any(mask):
        return X_aug

    raw = X_aug[mask] * std + mean
    rotations = sample_rotation_matrices(
        rng,
        int(mask.sum()),
        settings,
        windows=raw,
    )
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
        settings: AccelRotationSettings,
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
        self.settings = settings
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
            settings=self.settings,
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
        settings=settings,
        seed=int(cfg.get("seed", 42)),
        shuffle=True,
    )
    return TrainingInput(
        x=sequence,
        y=None,
        fit_kwargs={},
        augmentation_enabled=True,
    )
