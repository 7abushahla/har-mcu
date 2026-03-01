"""Post-training full-integer INT8 quantization."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import tensorflow as tf

from src.data.build_dataset import build_dataset_for_protocol
from src.data.io import dataset_exists, load_split_arrays
from src.train.train_baseline import train_baseline_for_protocol
from src.utils.artifacts import baseline_ckpt_path, ptq_tflite_path
from src.utils.config import apply_common_overrides, build_parser, ensure_path_dirs, load_yaml


def _representative_dataset(X_train: np.ndarray, n_samples: int):
    n = min(len(X_train), n_samples)
    for i in range(n):
        yield [X_train[i : i + 1].astype(np.float32)]


def quantize_ptq_for_protocol(
    cfg: dict[str, Any],
    window_size: int,
    protocol: str,
) -> dict[str, Any]:
    ensure_path_dirs(cfg)
    processed_dir = cfg["paths"]["processed_dir"]

    if not dataset_exists(processed_dir, window_size, protocol):
        build_dataset_for_protocol(cfg, window_size, protocol)

    ckpt_path = baseline_ckpt_path(cfg["paths"]["checkpoints_dir"], window_size, protocol)
    if not ckpt_path.exists():
        train_baseline_for_protocol(cfg, window_size, protocol)

    arrays = load_split_arrays(processed_dir, window_size, protocol)
    X_train = arrays["X_train"]

    model = tf.keras.models.load_model(ckpt_path)

    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    rep_count = int(cfg["quant"]["ptq"].get("representative_samples", 256))
    converter.representative_dataset = lambda: _representative_dataset(X_train, rep_count)

    if bool(cfg["quant"]["ptq"].get("enforce_full_int8", True)):
        converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
        converter.inference_input_type = tf.int8
        converter.inference_output_type = tf.int8

    tflite_blob = converter.convert()

    model_path = ptq_tflite_path(cfg["paths"]["models_tflite_dir"], window_size, protocol)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    model_path.write_bytes(tflite_blob)

    # Verify dtypes and capture model size.
    interp = tf.lite.Interpreter(model_path=str(model_path))
    input_dtype = str(interp.get_input_details()[0]["dtype"])
    output_dtype = str(interp.get_output_details()[0]["dtype"])

    fp32_size_kb = ckpt_path.stat().st_size / 1024.0
    int8_size_kb = model_path.stat().st_size / 1024.0

    reports_dir = Path(cfg["paths"]["reports_dir"])
    reports_dir.mkdir(parents=True, exist_ok=True)
    metrics = {
        "window_size": int(window_size),
        "protocol": protocol,
        "checkpoint": str(ckpt_path),
        "tflite_model": str(model_path),
        "fp32_checkpoint_size_kb": float(fp32_size_kb),
        "ptq_tflite_size_kb": float(int8_size_kb),
        "size_reduction_vs_ckpt_percent": float(100.0 * (1.0 - int8_size_kb / max(fp32_size_kb, 1e-9))),
        "input_dtype": input_dtype,
        "output_dtype": output_dtype,
        "representative_samples": int(rep_count),
    }

    json_path = reports_dir / f"ptq_export_T{window_size}_P{protocol}.json"
    md_path = reports_dir / f"ptq_export_T{window_size}_P{protocol}.md"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    with md_path.open("w", encoding="utf-8") as f:
        f.write(f"# PTQ Export (T={window_size}, protocol={protocol})\n\n")
        f.write(f"- Checkpoint: `{ckpt_path}`\n")
        f.write(f"- TFLite: `{model_path}`\n")
        f.write(f"- PTQ size: {int8_size_kb:.2f} KB\n")
        f.write(f"- Input dtype: `{input_dtype}`\n")
        f.write(f"- Output dtype: `{output_dtype}`\n")

    return {
        "tflite_model": str(model_path),
        "report_json": str(json_path),
        "report_md": str(md_path),
    }


def main() -> None:
    parser = build_parser("Export full-integer PTQ model")
    args = parser.parse_args()
    cfg = apply_common_overrides(load_yaml(args.config), args)

    ws = int(cfg["window_size_default"])
    for protocol in cfg.get("split_protocols", ["random_stratified"]):
        out = quantize_ptq_for_protocol(cfg, ws, protocol)
        print(f"PTQ done window_size={ws} protocol={protocol}")
        for k, v in out.items():
            print(f"  - {k}: {v}")


if __name__ == "__main__":
    main()
