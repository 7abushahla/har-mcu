"""Runtime environment checks."""

from __future__ import annotations

from typing import Any


def check_tensorflow_runtime(cfg: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "tensorflow_ok": False,
        "version_ok": False,
        "gpu_ok": False,
        "tensorflow_version": None,
        "gpus": [],
    }
    target_version = str(cfg.get("env", {}).get("tensorflow_version", "")).strip()
    require_gpu = bool(cfg.get("env", {}).get("require_gpu", False))

    try:
        import tensorflow as tf

        result["tensorflow_ok"] = True
        result["tensorflow_version"] = tf.__version__
        result["version_ok"] = target_version == "" or tf.__version__ == target_version
        gpus = tf.config.list_physical_devices("GPU")
        result["gpus"] = [g.name for g in gpus]
        result["gpu_ok"] = len(gpus) > 0
        if require_gpu and not result["gpu_ok"]:
            raise RuntimeError("No GPU visible to TensorFlow but env.require_gpu=true")
        if target_version and not result["version_ok"]:
            raise RuntimeError(
                f"TensorFlow version mismatch: expected {target_version}, got {tf.__version__}"
            )
    except Exception as exc:
        result["error"] = str(exc)
        if cfg.get("env", {}).get("require_gpu", False):
            raise

    return result
