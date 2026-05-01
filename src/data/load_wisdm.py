"""Load and validate WISDM raw CSV."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import pandas as pd

from src.data.load_har import load_har_dataframe
from src.utils.config import apply_common_overrides, build_parser, ensure_path_dirs, load_yaml


def load_wisdm_dataframe(cfg: dict[str, Any]) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Backward-compatible WISDM loader wrapper."""

    return load_har_dataframe(cfg, domain="wisdm", csv_path=Path(cfg["paths"]["raw_csv"]))


def main() -> None:
    parser = build_parser("Load WISDM CSV and print sanity header")
    args = parser.parse_args()

    cfg = apply_common_overrides(load_yaml(args.config), args)
    ensure_path_dirs(cfg)

    _, sanity = load_wisdm_dataframe(cfg)
    print("WISDM sanity header")
    for key, value in sanity.items():
        print(f"- {key}: {value}")


if __name__ == "__main__":
    main()
