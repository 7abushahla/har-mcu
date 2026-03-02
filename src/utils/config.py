"""Configuration helpers."""

from __future__ import annotations

import argparse
import copy
from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: str | Path) -> dict[str, Any]:
    path = Path(path).resolve()
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping at root of config: {path}")
    # Resolve relative paths in `paths:` against repo root.
    # Supports both configs/default.yaml and nested configs/papers/*.yaml.
    config_dir = path.parent
    if config_dir.name == "configs":
        repo_root = config_dir.parent
    elif config_dir.parent.name == "configs":
        repo_root = config_dir.parent.parent
    else:
        repo_root = config_dir

    if "paths" in data and isinstance(data["paths"], dict):
        for key, value in data["paths"].items():
            if isinstance(value, str) and value:
                p = Path(value)
                if not p.is_absolute():
                    data["paths"][key] = str((repo_root / p).resolve())
    return data


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(base)
    for key, value in override.items():
        if key in out and isinstance(out[key], dict) and isinstance(value, dict):
            out[key] = deep_merge(out[key], value)
        else:
            out[key] = value
    return out


def ensure_path_dirs(cfg: dict[str, Any]) -> None:
    paths = cfg.get("paths", {})
    for key, path_value in paths.items():
        if key.endswith("_dir"):
            Path(path_value).mkdir(parents=True, exist_ok=True)


def build_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--config", required=True, help="Path to yaml config")
    parser.add_argument("--window-size", type=int, default=None)
    parser.add_argument("--split-protocol", type=str, default=None)
    parser.add_argument("--label-policy", type=str, default=None)
    parser.add_argument("--run-mode", type=str, default=None, help="runtime.run_mode override")
    parser.add_argument("--smoke", action="store_true", help="Force smoke-mode settings")
    return parser


def apply_common_overrides(cfg: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    cfg = copy.deepcopy(cfg)
    if args.window_size is not None:
        cfg["window_size_default"] = int(args.window_size)
    if args.split_protocol is not None:
        cfg["split_protocols"] = [args.split_protocol]
    if args.label_policy is not None:
        cfg["label_policy"] = args.label_policy
    if args.run_mode is not None:
        cfg.setdefault("runtime", {})["run_mode"] = str(args.run_mode)
    if args.smoke:
        cfg.setdefault("smoke", {})["enabled"] = True
        cfg["train"]["epochs"] = int(cfg["smoke"].get("quick_epochs", 1))
    return cfg
