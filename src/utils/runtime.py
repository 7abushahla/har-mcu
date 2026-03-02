"""Runtime environment checks."""

from __future__ import annotations

from typing import Any


def check_tensorflow_runtime(cfg: dict[str, Any]) -> dict[str, Any]:
    runtime_cfg = cfg.get("runtime", {})
    run_mode = str(runtime_cfg.get("run_mode", "")).strip().lower()

    result: dict[str, Any] = {
        "tensorflow_ok": False,
        "version_ok": False,
        "gpu_ok": False,
        "tensorflow_version": None,
        "gpus": [],
        "run_mode": run_mode or None,
    }
    target_version = str(cfg.get("env", {}).get("tensorflow_version", "")).strip()
    require_gpu = bool(cfg.get("env", {}).get("require_gpu", False))
    # In full-run CPU mode, do not require GPU even if env.require_gpu is true.
    effective_require_gpu = require_gpu and run_mode != "full_run"
    result["require_gpu_effective"] = effective_require_gpu

    try:
        import tensorflow as tf

        result["tensorflow_ok"] = True
        result["tensorflow_version"] = tf.__version__
        result["version_ok"] = target_version == "" or tf.__version__ == target_version
        gpus = tf.config.list_physical_devices("GPU")
        result["gpus"] = [g.name for g in gpus]
        result["gpu_ok"] = len(gpus) > 0
        if effective_require_gpu and not result["gpu_ok"]:
            raise RuntimeError("No GPU visible to TensorFlow but env.require_gpu=true")
        if target_version and not result["version_ok"]:
            raise RuntimeError(
                f"TensorFlow version mismatch: expected {target_version}, got {tf.__version__}"
            )
    except Exception as exc:
        result["error"] = str(exc)
        if effective_require_gpu:
            raise

    return result
