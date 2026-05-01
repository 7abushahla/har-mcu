"""Build M3 datasets from merged M3 configs.

Run this inside Slurm jobs only. Configs under ``configs/m3`` are overlays with
``base_config`` and must be merged before calling the shared dataset builder.
"""

from __future__ import annotations

import argparse

from src.data.build_dataset import build_for_all_protocols
from src.m3.config import load_m3_config
from src.utils.config import apply_common_overrides, ensure_path_dirs


def _append_path_suffix(cfg: dict, suffix: str) -> None:
    if not suffix:
        return
    for key in ("processed_dir", "checkpoints_dir", "models_tflite_dir", "deploy_common_dir"):
        value = cfg.get("paths", {}).get(key)
        if value:
            cfg["paths"][key] = str(value).rstrip("/") + "/" + suffix.strip("/")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build processed datasets for M3")
    parser.add_argument("--config", required=True)
    parser.add_argument("--window-size", type=int, default=None)
    parser.add_argument("--split-protocol", type=str, default=None)
    parser.add_argument("--label-policy", type=str, default=None)
    parser.add_argument("--run-mode", type=str, default=None)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--max-windows-per-class", type=int, default=None)
    parser.add_argument(
        "--artifact-suffix",
        default=None,
        help="Append a suffix directory to generated artifact roots, e.g. smoke",
    )
    args = parser.parse_args()

    cfg = apply_common_overrides(load_m3_config(args.config), args)
    if args.max_windows_per_class is not None:
        cfg.setdefault("smoke", {})["max_windows_per_class"] = int(args.max_windows_per_class)
    if args.artifact_suffix:
        _append_path_suffix(cfg, args.artifact_suffix)
    ensure_path_dirs(cfg)

    outputs = build_for_all_protocols(cfg, window_size=cfg["window_size_default"])
    for out in outputs:
        print(f"Built dataset window_size={out['window_size']} protocol={out['protocol']}")
        for key, value in out["artifacts"].items():
            print(f"  - {key}: {value}")


if __name__ == "__main__":
    main()
