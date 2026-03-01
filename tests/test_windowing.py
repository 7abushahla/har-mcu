from __future__ import annotations

import numpy as np
import pandas as pd

from src.data.windowing import generate_windows


def _df() -> pd.DataFrame:
    rows = []
    for i in range(12):
        rows.append(
            {
                "user": 1,
                "activity": "Walking" if i < 6 else "Jogging",
                "timestamp": i + 1,
                "x-axis": float(i),
                "y-axis": float(i + 0.1),
                "z-axis": float(i + 0.2),
            }
        )
    return pd.DataFrame(rows)


def test_windowing_drop_boundary():
    class_to_idx = {"Walking": 0, "Jogging": 1}
    X, y, users, stats = generate_windows(
        _df(), window_size=4, overlap=0.5, label_policy="drop_cross_boundary", class_to_idx=class_to_idx
    )
    assert X.ndim == 3
    assert X.shape[-1] == 3
    assert len(X) == len(y) == len(users)
    assert stats["dropped_cross_boundary"] > 0


def test_windowing_majority_vote():
    class_to_idx = {"Walking": 0, "Jogging": 1}
    X, y, _, _ = generate_windows(
        _df(), window_size=4, overlap=0.5, label_policy="majority_vote", class_to_idx=class_to_idx
    )
    assert len(X) > 0
    assert set(np.unique(y)).issubset({0, 1})
