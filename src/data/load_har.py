"""General WISDM-style HAR CSV loading.

This loader accepts the shared raw schema used by WISDM and the Arduino/Tiny
Motion merged CSVs:

    user,activity,timestamp,x-axis,y-axis,z-axis
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from src.utils.constants import REQUIRED_WISDM_COLUMNS


def _path_for_domain(cfg: dict[str, Any], domain: str) -> Path:
    paths = cfg.get("paths", {})
    if domain == "arduino":
        return Path(paths.get("arduino_raw_csv", paths.get("raw_csv")))
    if domain == "wisdm":
        return Path(paths.get("wisdm_raw_csv", paths.get("raw_csv")))
    raise ValueError(f"Unsupported domain: {domain}")


def _coerce_users(df: pd.DataFrame, cfg: dict[str, Any]) -> tuple[pd.DataFrame, dict[str, Any]]:
    out = df.copy()
    out["original_user"] = out["user"].astype(str)

    user_map_cfg = cfg.get("data", {}).get("user_id_map", {})
    if user_map_cfg:
        mapping = {str(k): int(v) for k, v in user_map_cfg.items()}
        out["user"] = out["original_user"].map(mapping)
        missing = sorted(out.loc[out["user"].isna(), "original_user"].unique().tolist())
        if missing:
            raise ValueError(f"user_id_map missing users: {missing}")
        out["user"] = out["user"].astype(int)
        return out, {"user_id_map": mapping, "user_id_map_source": "config"}

    try:
        out["user"] = out["user"].astype(int)
        return out, {"user_id_map": {}, "user_id_map_source": "native_numeric"}
    except ValueError:
        unique_users = sorted(out["original_user"].unique().tolist())
        mapping = {name: 1000 + i for i, name in enumerate(unique_users)}
        out["user"] = out["original_user"].map(mapping).astype(int)
        return out, {"user_id_map": mapping, "user_id_map_source": "stable_auto"}


def load_har_dataframe(
    cfg: dict[str, Any],
    *,
    domain: str,
    csv_path: str | Path | None = None,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Load a WISDM-style HAR CSV and attach lightweight domain metadata."""

    path = Path(csv_path) if csv_path is not None else _path_for_domain(cfg, domain)
    if not path.exists():
        raise FileNotFoundError(f"HAR CSV not found: {path}")

    df = pd.read_csv(path)
    missing_cols = [c for c in REQUIRED_WISDM_COLUMNS if c not in df.columns]
    if missing_cols:
        raise ValueError(
            f"CSV missing required columns: {missing_cols}. Available columns: {list(df.columns)}"
        )

    df, user_meta = _coerce_users(df, cfg)
    df["domain"] = str(domain)
    df["source_csv"] = str(path)

    data_cfg = cfg.get("data", {})
    original_sample_rate_hz = float(data_cfg.get("sample_rate_hz", 20))
    target_sample_rate_hz = float(data_cfg.get("target_sample_rate_hz", original_sample_rate_hz))
    df["original_sample_rate_hz"] = original_sample_rate_hz
    df["target_sample_rate_hz"] = target_sample_rate_hz

    sanity = {
        "domain": str(domain),
        "source_csv": str(path),
        "rows": int(len(df)),
        "missing_values": int(df[REQUIRED_WISDM_COLUMNS].isna().sum().sum()),
        "zero_timestamps": int((df["timestamp"] == 0).sum()),
        "original_sample_rate_hz": original_sample_rate_hz,
        "target_sample_rate_hz": target_sample_rate_hz,
        "user_count": int(df["user"].nunique()),
        "users": sorted(int(u) for u in df["user"].unique().tolist()),
        **user_meta,
    }
    return df, sanity
