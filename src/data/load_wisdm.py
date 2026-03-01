"""Load and validate WISDM raw CSV."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import pandas as pd

from src.utils.config import apply_common_overrides, build_parser, ensure_path_dirs, load_yaml
from src.utils.constants import REQUIRED_WISDM_COLUMNS


def load_wisdm_dataframe(cfg: dict[str, Any]) -> tuple[pd.DataFrame, dict[str, int]]:
    csv_path = Path(cfg["paths"]["raw_csv"])
    if not csv_path.exists():
        raise FileNotFoundError(f"Raw CSV not found: {csv_path}")

    df = pd.read_csv(csv_path)
    missing_cols = [c for c in REQUIRED_WISDM_COLUMNS if c not in df.columns]
    if missing_cols:
        raise ValueError(
            f"CSV missing required columns: {missing_cols}. Available columns: {list(df.columns)}"
        )

    sanity = {
        "rows": int(len(df)),
        "missing_values": int(df[REQUIRED_WISDM_COLUMNS].isna().sum().sum()),
        "zero_timestamps": int((df["timestamp"] == 0).sum()),
    }
    return df, sanity


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
