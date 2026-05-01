"""Sampling-rate helpers for M3 HAR experiments."""

from __future__ import annotations

from typing import Any

import pandas as pd


def maybe_downsample_dataframe(
    df: pd.DataFrame,
    cfg: dict[str, Any],
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Downsample by deterministic integer stride when requested.

    This intentionally avoids interpolation for the first M3 implementation
    layer. Non-integer resampling should be added explicitly with tests before
    use in reported experiments.
    """

    data_cfg = cfg.get("data", {})
    source_hz = float(data_cfg.get("sample_rate_hz", 20))
    target_hz = float(data_cfg.get("target_sample_rate_hz", source_hz))
    downsample = bool(data_cfg.get("downsample", source_hz > target_hz))

    meta = {
        "sample_rate_hz": source_hz,
        "target_sample_rate_hz": target_hz,
        "downsample": downsample,
        "method": "none",
        "stride": 1,
        "rows_before": int(len(df)),
        "rows_after": int(len(df)),
    }

    if not downsample or source_hz == target_hz:
        return df, meta
    if target_hz <= 0 or source_hz <= 0:
        raise ValueError("sample rates must be positive")
    ratio = source_hz / target_hz
    stride = int(round(ratio))
    if abs(ratio - stride) > 1e-6 or stride <= 0:
        raise ValueError(
            f"Only integer-stride downsampling is supported, got {source_hz} -> {target_hz}"
        )

    work = df.sort_values(["user", "timestamp"]).copy()
    work["_row_order"] = range(len(work))
    keep = work.groupby(["user", "activity"], sort=False).cumcount() % stride == 0
    out = work.loc[keep].sort_values("_row_order").drop(columns=["_row_order"]).reset_index(drop=True)

    meta.update(
        {
            "method": "integer_stride",
            "stride": int(stride),
            "rows_after": int(len(out)),
        }
    )
    return out, meta
