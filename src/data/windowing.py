"""Window generation with configurable overlap and label policy."""

from __future__ import annotations

from collections import Counter
from typing import Any

import numpy as np
import pandas as pd

from src.utils.constants import AXIS_COLUMNS, LABEL_POLICIES


def _majority_label(values: np.ndarray) -> str:
    c = Counter(values.tolist())
    return c.most_common(1)[0][0]


def generate_windows(
    df: pd.DataFrame,
    window_size: int,
    overlap: float,
    label_policy: str,
    class_to_idx: dict[str, int],
    max_windows_per_class: int | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, int]]:
    if label_policy not in LABEL_POLICIES:
        raise ValueError(f"Unsupported label_policy: {label_policy}")
    if not (0.0 <= overlap < 1.0):
        raise ValueError("overlap must satisfy 0 <= overlap < 1")

    step = max(1, int(window_size * (1.0 - overlap)))

    xs: list[np.ndarray] = []
    ys: list[int] = []
    users: list[int] = []

    dropped_cross_boundary = 0
    dropped_unknown_label = 0
    candidate_windows = 0
    per_class_count: dict[int, int] = {v: 0 for v in class_to_idx.values()}

    # Build windows per user to avoid crossing subject boundaries.
    for user_id, group in df.groupby("user", sort=False):
        g = group.reset_index(drop=True)
        acts = g["activity"].values
        feats = g[AXIS_COLUMNS].values.astype(np.float32)
        for start in range(0, len(g) - window_size + 1, step):
            end = start + window_size
            candidate_windows += 1

            act_segment = acts[start:end]
            if label_policy == "drop_cross_boundary":
                if not np.all(act_segment == act_segment[0]):
                    dropped_cross_boundary += 1
                    continue
                label_name = str(act_segment[0])
            else:
                label_name = _majority_label(act_segment)

            if label_name not in class_to_idx:
                dropped_unknown_label += 1
                continue

            label_idx = class_to_idx[label_name]
            if max_windows_per_class is not None and per_class_count[label_idx] >= max_windows_per_class:
                continue

            xs.append(feats[start:end])
            ys.append(label_idx)
            users.append(int(user_id))
            per_class_count[label_idx] += 1

    X = np.asarray(xs, dtype=np.float32)
    y = np.asarray(ys, dtype=np.int64)
    user_ids = np.asarray(users, dtype=np.int32)

    stats = {
        "window_size": int(window_size),
        "step": int(step),
        "candidate_windows": int(candidate_windows),
        "windows_final": int(len(X)),
        "dropped_cross_boundary": int(dropped_cross_boundary),
        "dropped_unknown_label": int(dropped_unknown_label),
    }
    return X, y, user_ids, stats
