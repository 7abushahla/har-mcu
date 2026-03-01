"""Train/val/test split utilities for window-level data."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
from sklearn.model_selection import GroupShuffleSplit, train_test_split

from src.utils.artifacts import split_npz_path
from src.utils.repro import hash_split_payload


@dataclass
class SplitIndices:
    train: np.ndarray
    val: np.ndarray
    test: np.ndarray


def _check_non_empty(name: str, arr: np.ndarray) -> None:
    if len(arr) == 0:
        raise ValueError(f"{name} split is empty")


def make_random_stratified_split(
    y: np.ndarray,
    test_ratio: float,
    val_ratio_from_train: float,
    seed: int,
) -> SplitIndices:
    all_idx = np.arange(len(y))
    train_val_idx, test_idx = train_test_split(
        all_idx,
        test_size=test_ratio,
        random_state=seed,
        stratify=y,
    )
    train_idx, val_idx = train_test_split(
        train_val_idx,
        test_size=val_ratio_from_train,
        random_state=seed,
        stratify=y[train_val_idx],
    )

    _check_non_empty("train", train_idx)
    _check_non_empty("val", val_idx)
    _check_non_empty("test", test_idx)
    return SplitIndices(train=train_idx, val=val_idx, test=test_idx)


def make_user_holdout_split(
    y: np.ndarray,
    users: np.ndarray,
    test_ratio: float,
    val_ratio_from_train: float,
    seed: int,
) -> SplitIndices:
    idx = np.arange(len(y))

    gss_test = GroupShuffleSplit(n_splits=1, test_size=test_ratio, random_state=seed)
    train_val_idx, test_idx = next(gss_test.split(idx, y, groups=users))

    gss_val = GroupShuffleSplit(n_splits=1, test_size=val_ratio_from_train, random_state=seed)
    train_rel, val_rel = next(
        gss_val.split(train_val_idx, y[train_val_idx], groups=users[train_val_idx])
    )

    train_idx = train_val_idx[train_rel]
    val_idx = train_val_idx[val_rel]

    _check_non_empty("train", train_idx)
    _check_non_empty("val", val_idx)
    _check_non_empty("test", test_idx)
    return SplitIndices(train=train_idx, val=val_idx, test=test_idx)


def build_split(
    protocol: str,
    y: np.ndarray,
    users: np.ndarray,
    test_ratio: float,
    val_ratio_from_train: float,
    seed: int,
) -> SplitIndices:
    if protocol == "random_stratified":
        return make_random_stratified_split(y, test_ratio, val_ratio_from_train, seed)
    if protocol == "user_holdout":
        return make_user_holdout_split(y, users, test_ratio, val_ratio_from_train, seed)
    raise ValueError(f"Unsupported split protocol: {protocol}")


def save_split_indices(
    processed_dir: str,
    window_size: int,
    protocol: str,
    split: SplitIndices,
    payload: dict[str, Any],
) -> dict[str, Any]:
    path = split_npz_path(processed_dir, window_size, protocol)
    path.parent.mkdir(parents=True, exist_ok=True)

    split_hash = hash_split_payload(payload)
    np.savez(
        path,
        train=split.train,
        val=split.val,
        test=split.test,
        split_hash=split_hash,
    )

    meta = {
        "path": str(path),
        "split_hash": split_hash,
        "train_size": int(len(split.train)),
        "val_size": int(len(split.val)),
        "test_size": int(len(split.test)),
    }
    return meta
