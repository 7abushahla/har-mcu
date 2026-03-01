from __future__ import annotations

import numpy as np

from src.data.splits import build_split


def test_random_stratified_split_non_empty():
    y = np.array([0, 0, 1, 1, 2, 2, 0, 1, 2, 0, 1, 2])
    users = np.array([1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4])
    split = build_split("random_stratified", y, users, test_ratio=0.33, val_ratio_from_train=0.2, seed=42)
    assert len(split.train) > 0
    assert len(split.val) > 0
    assert len(split.test) > 0


def test_user_holdout_split_non_empty():
    y = np.array([0, 0, 1, 1, 2, 2, 0, 1, 2, 0, 1, 2])
    users = np.array([1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4])
    split = build_split("user_holdout", y, users, test_ratio=0.33, val_ratio_from_train=0.2, seed=42)
    assert len(split.train) > 0
    assert len(split.val) > 0
    assert len(split.test) > 0
