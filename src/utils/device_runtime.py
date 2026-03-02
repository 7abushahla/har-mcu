"""Stage-level runtime device policy helpers."""

from __future__ import annotations

from contextlib import contextmanager
from contextlib import nullcontext
from typing import Any, Iterator


STAGES = (
    "train",
    "eval_fp32",
    "ptq",
    "eval_ptq",
    "qat",
    "eval_qat",
)

_ALLOWED_RUN_MODES = {"sanity_check", "full_run"}
_DEFAULT_STAGE_DEVICES: dict[str, dict[str, str]] = {
    "sanity_check": {
        "train": "gpu",
        "eval_fp32": "gpu",
        "ptq": "gpu",
        "eval_ptq": "gpu",
        "qat": "cpu",
        "eval_qat": "cpu",
    },
    "full_run": {
        "train": "cpu",
        "eval_fp32": "cpu",
        "ptq": "cpu",
        "eval_ptq": "cpu",
        "qat": "cpu",
        "eval_qat": "cpu",
    },
}


def _load_tf(tf_module: Any | None = None) -> Any | None:
    if tf_module is not None:
        return tf_module
    try:
        import tensorflow as tf

        return tf
    except Exception:
        return None


def _normalize_stage_device(device: Any, *, stage: str, run_mode: str) -> str:
    normalized = str(device).strip().lower()
    if normalized not in {"cpu", "gpu"}:
        raise ValueError(
            f"Invalid runtime.stage_devices value for run_mode='{run_mode}', stage='{stage}': {device}"
        )
    return normalized


def _gpu_devices(tf_module: Any | None) -> list[str]:
    if tf_module is None:
        return []
    try:
        gpus = tf_module.config.list_physical_devices("GPU")
    except Exception:
        return []
    names: list[str] = []
    for gpu in gpus:
        names.append(str(getattr(gpu, "name", gpu)))
    return names


def resolve_run_mode(cfg: dict[str, Any]) -> str:
    runtime_cfg = cfg.get("runtime", {})
    run_mode = str(runtime_cfg.get("run_mode", "sanity_check")).strip().lower()
    if run_mode not in _ALLOWED_RUN_MODES:
        supported = ", ".join(sorted(_ALLOWED_RUN_MODES))
        raise ValueError(f"Unsupported runtime.run_mode '{run_mode}'. Supported: {supported}")
    return run_mode


def stage_device_map(cfg: dict[str, Any], run_mode: str | None = None) -> dict[str, str]:
    effective_mode = run_mode or resolve_run_mode(cfg)
    if effective_mode not in _DEFAULT_STAGE_DEVICES:
        supported = ", ".join(sorted(_DEFAULT_STAGE_DEVICES))
        raise ValueError(f"Unsupported run_mode '{effective_mode}'. Supported: {supported}")

    merged = dict(_DEFAULT_STAGE_DEVICES[effective_mode])
    runtime_cfg = cfg.get("runtime", {})
    stage_devices_cfg = runtime_cfg.get("stage_devices", {})
    mode_overrides = stage_devices_cfg.get(effective_mode, {}) if isinstance(stage_devices_cfg, dict) else {}

    if mode_overrides is not None and not isinstance(mode_overrides, dict):
        raise ValueError(
            f"runtime.stage_devices.{effective_mode} must be a mapping, got: {type(mode_overrides).__name__}"
        )

    for stage, value in (mode_overrides or {}).items():
        if stage not in STAGES:
            raise ValueError(f"Unknown runtime stage '{stage}' for run_mode '{effective_mode}'")
        merged[stage] = _normalize_stage_device(value, stage=stage, run_mode=effective_mode)

    missing = [stage for stage in STAGES if stage not in merged]
    if missing:
        raise ValueError(
            f"Missing runtime stage mappings for run_mode '{effective_mode}': {', '.join(missing)}"
        )
    return merged


def resolve_stage_device(cfg: dict[str, Any], stage: str, tf_module: Any | None) -> str:
    if stage not in STAGES:
        raise ValueError(f"Unknown runtime stage '{stage}'. Supported: {', '.join(STAGES)}")

    run_mode = resolve_run_mode(cfg)
    mapping = stage_device_map(cfg, run_mode)
    requested = mapping[stage]
    if requested == "cpu":
        return "cpu"

    runtime_cfg = cfg.get("runtime", {})
    gpu_fallback = bool(runtime_cfg.get("gpu_fallback_to_cpu", True))
    fail_if_gpu_missing = bool(runtime_cfg.get("fail_if_gpu_missing", False))
    gpus = _gpu_devices(tf_module)

    if gpus:
        return "gpu"
    if fail_if_gpu_missing:
        raise RuntimeError(
            f"Stage '{stage}' requested GPU in run_mode '{run_mode}', but no GPU is available."
        )
    if gpu_fallback:
        return "cpu"
    raise RuntimeError(
        f"Stage '{stage}' requested GPU in run_mode '{run_mode}', "
        "no GPU is available, and runtime.gpu_fallback_to_cpu=false."
    )


@contextmanager
def stage_device_scope(
    cfg: dict[str, Any],
    stage: str,
    tf_module: Any | None = None,
) -> Iterator[None]:
    tf_mod = _load_tf(tf_module)
    resolved = resolve_stage_device(cfg, stage, tf_module=tf_mod)

    if tf_mod is None:
        with nullcontext():
            yield
        return

    with tf_mod.device("/GPU:0" if resolved == "gpu" else "/CPU:0"):
        yield


def runtime_device_report(cfg: dict[str, Any], tf_module: Any | None = None) -> dict[str, Any]:
    run_mode = resolve_run_mode(cfg)
    tf_mod = _load_tf(tf_module)
    requested = stage_device_map(cfg, run_mode)
    resolved = {
        stage: resolve_stage_device(cfg, stage, tf_module=tf_mod)
        for stage in STAGES
    }
    gpus = _gpu_devices(tf_mod)

    runtime_cfg = cfg.get("runtime", {})
    return {
        "run_mode": run_mode,
        "gpu_available": bool(gpus),
        "gpus": gpus,
        "gpu_fallback_to_cpu": bool(runtime_cfg.get("gpu_fallback_to_cpu", True)),
        "fail_if_gpu_missing": bool(runtime_cfg.get("fail_if_gpu_missing", False)),
        "requested_stage_devices": requested,
        "resolved_stage_devices": resolved,
    }
