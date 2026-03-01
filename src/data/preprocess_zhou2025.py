"""Zhou 2025 preprocessing: drop nulls, drop zero timestamps, sort by user/timestamp."""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.utils.constants import REQUIRED_WISDM_COLUMNS


def preprocess_zhou2025(df: pd.DataFrame, cfg: dict[str, Any] | None = None) -> tuple[pd.DataFrame, dict[str, int]]:
    before_rows = int(len(df))
    cleaned = df.copy()

    cleaned = cleaned.dropna(subset=REQUIRED_WISDM_COLUMNS)
    after_dropna = int(len(cleaned))

    cleaned = cleaned[cleaned["timestamp"] != 0]
    after_drop_zero_ts = int(len(cleaned))

    cleaned = cleaned.sort_values(["user", "timestamp"], ascending=[True, True]).reset_index(drop=True)

    stats = {
        "rows_before": before_rows,
        "rows_after_dropna": after_dropna,
        "rows_after_drop_zero_timestamp": after_drop_zero_ts,
        "rows_final": int(len(cleaned)),
        "dropped_total": before_rows - int(len(cleaned)),
    }
    return cleaned, stats
