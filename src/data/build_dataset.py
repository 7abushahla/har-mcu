"""Build processed window datasets from local WISDM CSV."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np

from src.data.load_wisdm import load_wisdm_dataframe
from src.data.normalize import apply_axis_stats, fit_axis_stats
from src.data.preprocess_zhou2025 import preprocess_zhou2025
from src.data.splits import build_split, save_split_indices
from src.data.windowing import generate_windows
from src.utils.artifacts import arrays_prefix, datacard_path, norm_stats_path
from src.utils.config import apply_common_overrides, build_parser, ensure_path_dirs, load_yaml
from src.utils.constants import DEFAULT_CLASS_ORDER
from src.utils.repro import save_json, set_global_seed


def _save_arrays(prefix: Path, split_name: str, X: np.ndarray, y: np.ndarray) -> tuple[str, str]:
    x_path = prefix.parent / f"X_{split_name}_{prefix.name}.npy"
    y_path = prefix.parent / f"y_{split_name}_{prefix.name}.npy"
    np.save(x_path, X)
    np.save(y_path, y)
    return str(x_path), str(y_path)


def build_dataset_for_protocol(
    cfg: dict[str, Any],
    window_size: int,
    protocol: str,
) -> dict[str, Any]:
    set_global_seed(int(cfg["seed"]))

    raw_df, sanity = load_wisdm_dataframe(cfg)
    clean_df, pre_stats = preprocess_zhou2025(raw_df, cfg)

    class_order = cfg.get("classes") or DEFAULT_CLASS_ORDER
    class_to_idx = {name: i for i, name in enumerate(class_order)}

    max_windows = cfg.get("smoke", {}).get("max_windows_per_class")
    if max_windows is not None:
        max_windows = int(max_windows)

    X, y, users, win_stats = generate_windows(
        clean_df,
        window_size=window_size,
        overlap=float(cfg["overlap"]),
        label_policy=str(cfg.get("label_policy", "drop_cross_boundary")),
        class_to_idx=class_to_idx,
        max_windows_per_class=max_windows,
    )
    if len(X) == 0:
        raise RuntimeError("No windows generated; check window size and label policy")

    split = build_split(
        protocol=protocol,
        y=y,
        users=users,
        test_ratio=float(cfg["test_ratio"]),
        val_ratio_from_train=float(cfg["val_ratio_from_train"]),
        seed=int(cfg["seed"]),
    )

    split_meta = save_split_indices(
        processed_dir=cfg["paths"]["processed_dir"],
        window_size=window_size,
        protocol=protocol,
        split=split,
        payload={
            "seed": int(cfg["seed"]),
            "window_size": int(window_size),
            "protocol": protocol,
            "test_ratio": float(cfg["test_ratio"]),
            "val_ratio_from_train": float(cfg["val_ratio_from_train"]),
            "label_policy": str(cfg.get("label_policy", "drop_cross_boundary")),
        },
    )

    X_train_raw = X[split.train]
    X_val_raw = X[split.val]
    X_test_raw = X[split.test]

    y_train = y[split.train]
    y_val = y[split.val]
    y_test = y[split.test]

    mean, std = fit_axis_stats(X_train_raw)
    X_train = apply_axis_stats(X_train_raw, mean, std)
    X_val = apply_axis_stats(X_val_raw, mean, std)
    X_test = apply_axis_stats(X_test_raw, mean, std)

    processed_dir = Path(cfg["paths"]["processed_dir"])
    prefix = arrays_prefix(processed_dir, window_size, protocol)

    artifacts = {}
    artifacts["X_train"], artifacts["y_train"] = _save_arrays(prefix, "train", X_train, y_train)
    artifacts["X_val"], artifacts["y_val"] = _save_arrays(prefix, "val", X_val, y_val)
    artifacts["X_test"], artifacts["y_test"] = _save_arrays(prefix, "test", X_test, y_test)

    stats_path = norm_stats_path(processed_dir, window_size, protocol)
    norm_payload = {
        "axis_columns": ["x-axis", "y-axis", "z-axis"],
        "mean": mean.reshape(-1).tolist(),
        "std": std.reshape(-1).tolist(),
        "class_order": class_order,
        "window_size": int(window_size),
        "protocol": protocol,
    }
    save_json(stats_path, norm_payload)
    artifacts["norm_stats"] = str(stats_path)

    counts = {
        class_order[i]: {
            "train": int((y_train == i).sum()),
            "val": int((y_val == i).sum()),
            "test": int((y_test == i).sum()),
        }
        for i in range(len(class_order))
    }

    card_path = datacard_path(processed_dir, window_size, protocol)
    datacard = {
        "raw_sanity": sanity,
        "preprocess": pre_stats,
        "windowing": win_stats,
        "split": split_meta,
        "classes": class_order,
        "counts": counts,
    }
    save_json(card_path, datacard)
    artifacts["datacard"] = str(card_path)

    return {
        "window_size": int(window_size),
        "protocol": protocol,
        "artifacts": artifacts,
        "split": split_meta,
        "datacard": datacard,
    }


def build_for_all_protocols(cfg: dict[str, Any], window_size: int | None = None) -> list[dict[str, Any]]:
    ensure_path_dirs(cfg)
    protocols = cfg.get("split_protocols", ["random_stratified"])
    if isinstance(protocols, str):
        protocols = [protocols]
    ws = int(window_size if window_size is not None else cfg["window_size_default"])
    return [build_dataset_for_protocol(cfg, ws, p) for p in protocols]


def main() -> None:
    parser = build_parser("Build processed datasets for HAR pipeline")
    args = parser.parse_args()

    cfg = apply_common_overrides(load_yaml(args.config), args)
    ensure_path_dirs(cfg)

    outputs = build_for_all_protocols(cfg, window_size=cfg["window_size_default"])
    for out in outputs:
        print(f"Built dataset window_size={out['window_size']} protocol={out['protocol']}")
        for k, v in out["artifacts"].items():
            print(f"  - {k}: {v}")


if __name__ == "__main__":
    main()
