"""Build processed window datasets from local WISDM CSV."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np

from src.data.load_har import load_har_dataframe
from src.data.normalize import apply_axis_stats, fit_axis_stats
from src.data.preprocess_zhou2025 import preprocess_zhou2025
from src.data.resample import maybe_downsample_dataframe
from src.data.splits import build_split, save_split_indices
from src.data.units import apply_unit_transform
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


def _active_domain(cfg: dict[str, Any]) -> str:
    data_cfg = cfg.get("data", {})
    source = str(data_cfg.get("source", "wisdm"))
    if source == "arduino":
        return "arduino"
    if source == "wisdm_arduino":
        return str(data_cfg.get("train_domain", "wisdm"))
    return "wisdm"


def _load_prepared_dataframe(cfg: dict[str, Any]) -> tuple[Any, dict[str, Any]]:
    domain = _active_domain(cfg)
    raw_df, raw_sanity = load_har_dataframe(cfg, domain=domain)
    clean_df, pre_stats = preprocess_zhou2025(raw_df, cfg)
    unit_df, unit_meta = apply_unit_transform(clean_df, cfg, domain=domain)
    sampled_df, sampling_meta = maybe_downsample_dataframe(unit_df, cfg)
    data_meta = {
        "domain": domain,
        "raw_sanity": raw_sanity,
        "preprocess": pre_stats,
        "unit_transform": unit_meta,
        "sampling": sampling_meta,
    }
    return sampled_df, data_meta


def build_dataset_for_protocol(
    cfg: dict[str, Any],
    window_size: int,
    protocol: str,
    normalization_stats: dict[str, Any] | None = None,
    normalization_stats_source: str | None = None,
) -> dict[str, Any]:
    set_global_seed(int(cfg["seed"]))

    clean_df, data_meta = _load_prepared_dataframe(cfg)

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
    target_sample_rate_hz = float(cfg.get("data", {}).get("target_sample_rate_hz", 20))
    win_stats.update(
        {
            "sample_rate_hz": float(cfg.get("data", {}).get("sample_rate_hz", target_sample_rate_hz)),
            "target_sample_rate_hz": target_sample_rate_hz,
            "window_size_samples": int(window_size),
            "window_duration_seconds": float(window_size) / target_sample_rate_hz,
            "overlap": float(cfg["overlap"]),
        }
    )

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

    normalization_cfg = cfg.get("normalization", {})
    normalization_mode = str(normalization_cfg.get("mode", "train_zscore"))
    if normalization_mode == "train_zscore":
        if normalization_stats is None:
            mean, std = fit_axis_stats(X_train_raw)
            stats_source = "local_train_split"
        else:
            mean = np.asarray(normalization_stats["mean"], dtype=np.float32).reshape(1, 1, -1)
            std = np.asarray(normalization_stats["std"], dtype=np.float32).reshape(1, 1, -1)
            if mean.shape[-1] != X_train_raw.shape[-1] or std.shape[-1] != X_train_raw.shape[-1]:
                raise ValueError(
                    "External normalization stats feature count does not match dataset features"
                )
            stats_source = normalization_stats_source or "external_train_split"
        X_train = apply_axis_stats(X_train_raw, mean, std)
        X_val = apply_axis_stats(X_val_raw, mean, std)
        X_test = apply_axis_stats(X_test_raw, mean, std)
        inference_norm_applied = not bool(
            normalization_cfg.get("diagnostic_skip_inference_norm", False)
        )
    elif normalization_mode == "none":
        mean = np.zeros((1, 1, X_train_raw.shape[-1]), dtype=np.float32)
        std = np.ones((1, 1, X_train_raw.shape[-1]), dtype=np.float32)
        X_train = X_train_raw.astype(np.float32)
        X_val = X_val_raw.astype(np.float32)
        X_test = X_test_raw.astype(np.float32)
        inference_norm_applied = False
        stats_source = "none"
    else:
        raise ValueError(f"Unsupported normalization.mode: {normalization_mode}")

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
        "normalization_mode": normalization_mode,
        "normalization_stats_source": stats_source,
        "inference_norm_applied": bool(inference_norm_applied),
        "diagnostic_skip_inference_norm": bool(
            normalization_cfg.get("diagnostic_skip_inference_norm", False)
        ),
        "diagnostic_only": bool(cfg.get("m3", {}).get("diagnostic_only", False)),
        "class_order": class_order,
        "window_size": int(window_size),
        "window_size_samples": int(window_size),
        "window_duration_seconds": win_stats["window_duration_seconds"],
        "protocol": protocol,
        "data": data_meta,
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
        "data": data_meta,
        "raw_sanity": data_meta["raw_sanity"],
        "preprocess": data_meta["preprocess"],
        "windowing": win_stats,
        "split": split_meta,
        "normalization": {
            "mode": normalization_mode,
            "norm_stats": str(stats_path),
            "normalization_stats_source": stats_source,
            "inference_norm_applied": bool(inference_norm_applied),
            "diagnostic_skip_inference_norm": bool(
                normalization_cfg.get("diagnostic_skip_inference_norm", False)
            ),
            "diagnostic_only": bool(cfg.get("m3", {}).get("diagnostic_only", False)),
        },
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
