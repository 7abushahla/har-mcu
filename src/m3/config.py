"""Config loading and validation for Milestone 3 experiments.

This module intentionally performs config-only validation. It must not load
datasets or inspect CSV schemas; those operations belong inside Slurm jobs.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.utils.config import deep_merge, load_yaml
from src.utils.constants import DEFAULT_CLASS_ORDER


VALID_DATA_SOURCES = {"wisdm", "arduino", "wisdm_arduino"}
VALID_DOMAINS = {"wisdm", "arduino"}
VALID_SPLITS = {"random_stratified", "user_holdout"}
VALID_TRANSFER_MODES = {
    "source_only",
    "zero_shot",
    "finetune",
    "arduino_from_scratch",
}
VALID_UNIT_MODES = {
    "raw_no_conversion",
    "arduino_g",
    "wisdm_to_g",
    "arduino_to_mps2_legacy",
}
VALID_NORM_MODES = {"train_zscore", "none"}

M3_MASTER_COLUMNS = [
    "experiment_id",
    "model_variant",
    "data_source",
    "train_domain",
    "eval_domain",
    "sample_rate_hz",
    "target_sample_rate_hz",
    "downsample",
    "window_size_samples",
    "window_duration_seconds",
    "overlap",
    "unit_mode",
    "normalization_mode",
    "inference_norm_applied",
    "split_protocol",
    "transfer_mode",
    "seed",
    "fp32_accuracy",
    "fp32_macro_f1",
    "ptq_accuracy",
    "ptq_macro_f1",
    "qat_accuracy",
    "qat_macro_f1",
    "model_size_kb",
    "latency_mean_ms",
    "latency_median_ms",
    "latency_p95_ms",
    "deploy_gate_status",
    "notes",
]


@dataclass(frozen=True)
class M3ConfigSummary:
    """Human-readable summary for dry-run output."""

    experiment_id: str
    model_variant: str
    data_source: str
    train_domain: str
    eval_domain: str
    transfer_mode: str
    split_protocols: list[str]
    window_size_samples: int
    window_duration_seconds: float
    sample_rate_hz: float
    target_sample_rate_hz: float
    unit_mode: str
    normalization_mode: str
    diagnostic_only: bool
    enabled: bool
    tooling_only: bool


def repo_root_from_config(config_path: str | Path) -> Path:
    """Infer repo root from a config path under configs/ or configs/m3/."""

    path = Path(config_path).resolve()
    for parent in [path.parent, *path.parents]:
        if (parent / "pyproject.toml").exists() and (parent / "src").is_dir():
            return parent
    return Path.cwd()


def load_m3_config(config_path: str | Path) -> dict[str, Any]:
    """Load an M3 config, optionally deep-merging with ``base_config``.

    M3 config files are intentionally small overrides. By default they merge
    onto ``configs/default.yaml`` so existing DeepConvLSTM defaults remain the
    starting point.
    """

    config_path = Path(config_path).resolve()
    override = load_yaml(config_path)
    repo_root = repo_root_from_config(config_path)
    base_value = override.pop("base_config", "configs/default.yaml")
    base_path = Path(base_value)
    if not base_path.is_absolute():
        base_path = repo_root / base_path
    base = load_yaml(base_path)
    cfg = deep_merge(base, override)
    cfg.setdefault("m3", {})["config_path"] = str(config_path)
    cfg.setdefault("m3", {})["base_config"] = str(base_path)
    return cfg


def _get(cfg: dict[str, Any], dotted: str, default: Any = None) -> Any:
    cur: Any = cfg
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _window_duration(window_size: int, target_sample_rate_hz: float) -> float:
    if target_sample_rate_hz <= 0:
        return 0.0
    return float(window_size) / float(target_sample_rate_hz)


def validate_m3_config(cfg: dict[str, Any]) -> list[str]:
    """Return validation errors. An empty list means the config contract passes."""

    errors: list[str] = []

    experiment_id = _get(cfg, "m3.experiment_id")
    if not experiment_id:
        errors.append("m3.experiment_id is required")

    classes = cfg.get("classes")
    if classes != DEFAULT_CLASS_ORDER:
        errors.append(f"classes must equal {DEFAULT_CLASS_ORDER!r}")

    if float(cfg.get("overlap", -1.0)) != 0.5:
        errors.append("overlap must be exactly 0.5 for M3")

    data_source = _get(cfg, "data.source")
    if data_source not in VALID_DATA_SOURCES:
        errors.append(f"data.source must be one of {sorted(VALID_DATA_SOURCES)}")

    train_domain = _get(cfg, "data.train_domain")
    eval_domain = _get(cfg, "data.eval_domain")
    if train_domain not in VALID_DOMAINS:
        errors.append(f"data.train_domain must be one of {sorted(VALID_DOMAINS)}")
    if eval_domain not in VALID_DOMAINS:
        errors.append(f"data.eval_domain must be one of {sorted(VALID_DOMAINS)}")

    transfer_mode = _get(cfg, "m3.transfer_mode")
    if transfer_mode not in VALID_TRANSFER_MODES:
        errors.append(f"m3.transfer_mode must be one of {sorted(VALID_TRANSFER_MODES)}")

    unit_mode = _get(cfg, "data.unit_mode")
    domain_unit_modes = _get(cfg, "data.domain_unit_modes", {})
    if unit_mode not in VALID_UNIT_MODES and not domain_unit_modes:
        errors.append(
            "data.unit_mode must be an explicit unit mode unless "
            "data.domain_unit_modes is provided"
        )
    if isinstance(domain_unit_modes, dict):
        for domain, mode in domain_unit_modes.items():
            if domain not in VALID_DOMAINS:
                errors.append(f"data.domain_unit_modes has unsupported domain: {domain}")
            if mode not in VALID_UNIT_MODES:
                errors.append(f"unit mode for domain {domain!r} is unsupported: {mode!r}")

    norm_mode = _get(cfg, "normalization.mode")
    if norm_mode not in VALID_NORM_MODES:
        errors.append(f"normalization.mode must be one of {sorted(VALID_NORM_MODES)}")

    if bool(_get(cfg, "normalization.diagnostic_skip_inference_norm", False)):
        if not bool(_get(cfg, "m3.diagnostic_only", False)):
            errors.append(
                "normalization.diagnostic_skip_inference_norm=true requires "
                "m3.diagnostic_only=true"
            )

    protocols = _as_list(cfg.get("split_protocols"))
    if not protocols:
        errors.append("split_protocols must contain at least one protocol")
    for protocol in protocols:
        if protocol not in VALID_SPLITS:
            errors.append(f"unsupported split protocol: {protocol!r}")

    sample_rate_hz = float(_get(cfg, "data.sample_rate_hz", 0.0) or 0.0)
    target_sample_rate_hz = float(_get(cfg, "data.target_sample_rate_hz", 0.0) or 0.0)
    if sample_rate_hz <= 0:
        errors.append("data.sample_rate_hz must be positive")
    if target_sample_rate_hz <= 0:
        errors.append("data.target_sample_rate_hz must be positive")

    window_size = int(cfg.get("window_size_default", 0) or 0)
    if window_size <= 0:
        errors.append("window_size_default must be positive")
    duration = _window_duration(window_size, target_sample_rate_hz)
    configured_duration = _get(cfg, "data.window_duration_seconds")
    if configured_duration is not None:
        if abs(float(configured_duration) - duration) > 1e-6:
            errors.append(
                "data.window_duration_seconds must equal "
                "window_size_default / data.target_sample_rate_hz"
            )

    if _get(cfg, "quant.ptq.representative_source", "train") != "train":
        errors.append("quant.ptq.representative_source must remain train for M3")
    if _get(cfg, "quant.qat.representative_source", "train") != "train":
        errors.append("quant.qat.representative_source must remain train for M3")

    if "paths" not in cfg:
        errors.append("paths section is required")
    else:
        if not _get(cfg, "paths.wisdm_raw_csv"):
            errors.append("paths.wisdm_raw_csv is required")
        if data_source in {"arduino", "wisdm_arduino"} and not _get(
            cfg, "paths.arduino_raw_csv"
        ):
            errors.append("paths.arduino_raw_csv is required for Arduino experiments")

    return errors


def summarize_m3_config(cfg: dict[str, Any]) -> M3ConfigSummary:
    """Build the dry-run summary without touching datasets."""

    target_sample_rate_hz = float(_get(cfg, "data.target_sample_rate_hz"))
    window_size = int(cfg["window_size_default"])
    return M3ConfigSummary(
        experiment_id=str(_get(cfg, "m3.experiment_id")),
        model_variant=str(_get(cfg, "experiment.model_variant")),
        data_source=str(_get(cfg, "data.source")),
        train_domain=str(_get(cfg, "data.train_domain")),
        eval_domain=str(_get(cfg, "data.eval_domain")),
        transfer_mode=str(_get(cfg, "m3.transfer_mode")),
        split_protocols=[str(x) for x in _as_list(cfg.get("split_protocols"))],
        window_size_samples=window_size,
        window_duration_seconds=_window_duration(window_size, target_sample_rate_hz),
        sample_rate_hz=float(_get(cfg, "data.sample_rate_hz")),
        target_sample_rate_hz=target_sample_rate_hz,
        unit_mode=str(_get(cfg, "data.unit_mode")),
        normalization_mode=str(_get(cfg, "normalization.mode")),
        diagnostic_only=bool(_get(cfg, "m3.diagnostic_only", False)),
        enabled=bool(_get(cfg, "m3.enabled", True)),
        tooling_only=bool(_get(cfg, "m3.tooling_only", False)),
    )


def discover_m3_configs(config_dir: str | Path) -> list[Path]:
    """Return E*.yaml M3 experiment configs in deterministic order."""

    root = Path(config_dir)
    return sorted(p for p in root.glob("E*.yaml") if p.is_file())
