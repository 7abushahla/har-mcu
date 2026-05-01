"""Explicit unit-convention transforms for M3 datasets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd

from src.utils.constants import AXIS_COLUMNS


@dataclass(frozen=True)
class UnitTransform:
    domain: str
    unit_mode: str
    pre_multiply: float
    scale: float

    @property
    def total_scale(self) -> float:
        return float(self.pre_multiply) * float(self.scale)


def unit_mode_for_domain(cfg: dict[str, Any], domain: str) -> str:
    data_cfg = cfg.get("data", {})
    domain_modes = data_cfg.get("domain_unit_modes", {})
    if isinstance(domain_modes, dict) and domain in domain_modes:
        return str(domain_modes[domain])
    return str(data_cfg.get("unit_mode", "raw_no_conversion"))


def unit_transform_for_domain(cfg: dict[str, Any], domain: str) -> UnitTransform:
    """Return the explicit scale transform for a domain."""

    mode = unit_mode_for_domain(cfg, domain)
    data_cfg = cfg.get("data", {})
    configured = data_cfg.get("unit_scales", {}).get(domain, {})

    if mode == "raw_no_conversion":
        pre_multiply = float(configured.get("pre_multiply", 1.0))
        scale = float(configured.get("scale", 1.0))
    elif mode == "arduino_g":
        pre_multiply = float(configured.get("pre_multiply", 4.0 if domain == "arduino" else 1.0))
        scale = float(configured.get("scale", 1.0))
    elif mode == "wisdm_to_g":
        factor = float(configured.get("factor", configured.get("divisor", 9.80665)))
        pre_multiply = float(configured.get("pre_multiply", 1.0))
        scale = float(configured.get("scale", 1.0 / factor))
    elif mode == "arduino_to_mps2_legacy":
        pre_multiply = float(configured.get("pre_multiply", 4.0 if domain == "arduino" else 1.0))
        scale = float(configured.get("scale", 9.80665 if domain == "arduino" else 1.0))
    else:
        raise ValueError(f"Unsupported unit mode: {mode}")

    return UnitTransform(
        domain=str(domain),
        unit_mode=mode,
        pre_multiply=pre_multiply,
        scale=scale,
    )


def apply_unit_transform(
    df: pd.DataFrame,
    cfg: dict[str, Any],
    *,
    domain: str,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    transform = unit_transform_for_domain(cfg, domain)
    out = df.copy()
    total = transform.total_scale
    if total != 1.0:
        out.loc[:, AXIS_COLUMNS] = out[AXIS_COLUMNS].astype(float) * total
    out["unit_mode"] = transform.unit_mode
    meta = {
        "domain": transform.domain,
        "unit_mode": transform.unit_mode,
        "pre_multiply": float(transform.pre_multiply),
        "scale": float(transform.scale),
        "total_scale": float(transform.total_scale),
        "axis_columns": list(AXIS_COLUMNS),
    }
    return out, meta
