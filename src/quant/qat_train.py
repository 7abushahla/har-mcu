"""Quantization-aware training with fallback compatibility paths."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import tensorflow as tf

from src.data.build_dataset import build_dataset_for_protocol
from src.data.io import dataset_exists, load_split_arrays
from src.train.train_baseline import train_baseline_for_protocol
from src.utils.artifacts import baseline_ckpt_path, qat_tflite_path
from src.utils.config import apply_common_overrides, build_parser, ensure_path_dirs, load_yaml


def _representative_dataset(X_train: np.ndarray, n_samples: int):
    n = min(len(X_train), n_samples)
    for i in range(n):
        yield [X_train[i : i + 1].astype(np.float32)]


def _build_qat_model(fp32_model: tf.keras.Model) -> tuple[tf.keras.Model, str]:
    import tensorflow_model_optimization as tfmot

    try:
        qat_model = tfmot.quantization.keras.quantize_model(fp32_model)
        return qat_model, "quantize_model_full"
    except Exception:
        quantize_annotate_layer = tfmot.quantization.keras.quantize_annotate_layer
        quantize_apply = tfmot.quantization.keras.quantize_apply

        def annotate(layer: tf.keras.layers.Layer) -> tf.keras.layers.Layer:
            if isinstance(layer, (tf.keras.layers.Conv1D, tf.keras.layers.Dense)):
                return quantize_annotate_layer(layer)
            return layer

        annotated = tf.keras.models.clone_model(fp32_model, clone_function=annotate)
        annotated.set_weights(fp32_model.get_weights())
        qat_model = quantize_apply(annotated)
        return qat_model, "annotate_conv_dense_only"


def qat_for_protocol(
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
    X_train, y_train = arrays["X_train"], arrays["y_train"]
    X_val, y_val = arrays["X_val"], arrays["y_val"]

    num_classes = len(cfg.get("classes", [])) or int(np.max(y_train)) + 1
    y_train_oh = tf.keras.utils.to_categorical(y_train, num_classes)
    y_val_oh = tf.keras.utils.to_categorical(y_val, num_classes)

    fp32_model = tf.keras.models.load_model(ckpt_path)

    notes: list[str] = []
    try:
        qat_model, strategy = _build_qat_model(fp32_model)
        notes.append(f"QAT strategy: {strategy}")
    except Exception as exc:
        notes.append(f"QAT model construction failed: {exc}")
        raise RuntimeError("Unable to construct QAT model") from exc

    qat_model.compile(
        optimizer=tf.keras.optimizers.RMSprop(
            learning_rate=float(cfg["quant"]["qat"].get("learning_rate", 1e-4))
        ),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    hist = qat_model.fit(
        X_train,
        y_train_oh,
        validation_data=(X_val, y_val_oh),
        epochs=int(cfg["quant"]["qat"].get("epochs", 10)),
        batch_size=int(cfg["quant"]["qat"].get("batch_size", cfg["train"].get("batch_size", 64))),
        verbose=2,
    )

    ckpt_dir = Path(cfg["paths"]["checkpoints_dir"])
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    qat_ckpt = ckpt_dir / f"deepconv_lstm_qat_T{window_size}_P{protocol}.keras"
    qat_model.save(qat_ckpt)

    tfl_path = qat_tflite_path(cfg["paths"]["models_tflite_dir"], window_size, protocol)
    tfl_path.parent.mkdir(parents=True, exist_ok=True)

    converter = tf.lite.TFLiteConverter.from_keras_model(qat_model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.representative_dataset = lambda: _representative_dataset(
        X_train, int(cfg["quant"]["ptq"].get("representative_samples", 256))
    )

    deployable_full_int8 = False
    try:
        converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
        converter.inference_input_type = tf.int8
        converter.inference_output_type = tf.int8
        tfl_blob = converter.convert()
        deployable_full_int8 = True
        notes.append("Exported as full INT8 model")
    except Exception as exc:
        notes.append(f"Full INT8 export failed: {exc}")
        converter = tf.lite.TFLiteConverter.from_keras_model(qat_model)
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        tfl_blob = converter.convert()
        notes.append("Fell back to non-full-int8 export (not guaranteed TFLM deployable)")

    tfl_path.write_bytes(tfl_blob)

    # Capture converter output dtypes where possible.
    input_dtype = "unknown"
    output_dtype = "unknown"
    try:
        interp = tf.lite.Interpreter(model_path=str(tfl_path))
        input_dtype = str(interp.get_input_details()[0]["dtype"])
        output_dtype = str(interp.get_output_details()[0]["dtype"])
    except Exception as exc:
        notes.append(f"Could not inspect QAT TFLite dtypes: {exc}")

    reports_dir = Path(cfg["paths"]["reports_dir"])
    reports_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        "window_size": int(window_size),
        "protocol": protocol,
        "qat_checkpoint": str(qat_ckpt),
        "qat_tflite": str(tfl_path),
        "input_dtype": input_dtype,
        "output_dtype": output_dtype,
        "deployable_full_int8": bool(deployable_full_int8),
        "epochs_ran": int(len(hist.history.get("loss", []))),
        "notes": notes,
    }

    json_path = reports_dir / f"qat_export_T{window_size}_P{protocol}.json"
    md_path = reports_dir / f"qat_vs_ptq_T{window_size}_P{protocol}.md"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    with md_path.open("w", encoding="utf-8") as f:
        f.write(f"# QAT Export (T={window_size}, protocol={protocol})\n\n")
        f.write(f"- QAT checkpoint: `{qat_ckpt}`\n")
        f.write(f"- QAT tflite: `{tfl_path}`\n")
        f.write(f"- Full INT8 deployable: `{deployable_full_int8}`\n")
        f.write(f"- Input dtype: `{input_dtype}`\n")
        f.write(f"- Output dtype: `{output_dtype}`\n\n")
        f.write("## Notes\n\n")
        for note in notes:
            f.write(f"- {note}\n")

    return {"report_json": str(json_path), "report_md": str(md_path), "tflite": str(tfl_path)}


def main() -> None:
    parser = build_parser("Run QAT fine-tuning and export")
    args = parser.parse_args()
    cfg = apply_common_overrides(load_yaml(args.config), args)

    ws = int(cfg["window_size_default"])
    for protocol in cfg.get("split_protocols", ["random_stratified"]):
        out = qat_for_protocol(cfg, ws, protocol)
        print(f"QAT done window_size={ws} protocol={protocol}")
        for k, v in out.items():
            print(f"  - {k}: {v}")


if __name__ == "__main__":
    main()
