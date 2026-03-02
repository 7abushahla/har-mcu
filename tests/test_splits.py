from __future__ import annotations

import numpy as np

from src.data.splits import build_split


def _labels_and_users() -> tuple[np.ndarray, np.ndarray]:
    # 6 users, each contributes two samples per class (0,1,2).
    y_blocks = []
    u_blocks = []
    for user in range(1, 7):
        y_blocks.append(np.array([0, 0, 1, 1, 2, 2], dtype=np.int64))
        u_blocks.append(np.full(6, user, dtype=np.int64))
    return np.concatenate(y_blocks), np.concatenate(u_blocks)


def test_random_stratified_split_non_empty():
    y, users = _labels_and_users()
    split = build_split("random_stratified", y, users, test_ratio=0.33, val_ratio_from_train=0.2, seed=42)
    assert len(split.train) > 0
    assert len(split.val) > 0
    assert len(split.test) > 0


def test_user_holdout_split_non_empty():
    y, users = _labels_and_users()
    split = build_split("user_holdout", y, users, test_ratio=0.33, val_ratio_from_train=0.2, seed=42)
    assert len(split.train) > 0
    assert len(split.val) > 0
    assert len(split.test) > 0


def test_user_holdout_has_no_user_leakage():
    y, users = _labels_and_users()
    split = build_split("user_holdout", y, users, test_ratio=0.33, val_ratio_from_train=0.2, seed=42)

    train_users = set(users[split.train].tolist())
    val_users = set(users[split.val].tolist())
    test_users = set(users[split.test].tolist())

    assert train_users.isdisjoint(val_users)
    assert train_users.isdisjoint(test_users)
    assert val_users.isdisjoint(test_users)
