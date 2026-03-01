#!/usr/bin/env python3
"""Validate TensorFlow version and CUDA GPU visibility."""

from __future__ import annotations

import argparse
import json
import subprocess


def _run_cmd(cmd: list[str]) -> str:
    try:
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True).strip()
    except Exception as exc:
        return f"error: {exc}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Check TensorFlow CUDA runtime")
    parser.add_argument("--expect-version", default="2.14.1")
    parser.add_argument("--require-gpu", action="store_true")
    parser.add_argument("--out", default="reports/tf_cuda_check.json")
    args = parser.parse_args()

    payload = {
        "expected_tensorflow_version": args.expect_version,
        "require_gpu": bool(args.require_gpu),
    }

    exit_code = 0
    try:
        import tensorflow as tf

        payload["tensorflow_version"] = tf.__version__
        payload["version_ok"] = tf.__version__ == args.expect_version

        gpus = tf.config.list_physical_devices("GPU")
        payload["visible_gpus"] = [g.name for g in gpus]
        payload["gpu_ok"] = len(gpus) > 0

        payload["tf_build_info"] = dict(tf.sysconfig.get_build_info())
    except Exception as exc:
        payload["import_ok"] = False
        payload["error"] = str(exc)
        payload["version_ok"] = False
        payload["gpu_ok"] = False
        exit_code = 1
    else:
        payload["import_ok"] = True
        if not payload["version_ok"]:
            exit_code = 1
        if args.require_gpu and not payload["gpu_ok"]:
            exit_code = 1

    payload["nvidia_smi"] = _run_cmd(["nvidia-smi", "--query-gpu=name,driver_version", "--format=csv,noheader"])

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(json.dumps(payload, indent=2))
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
