"""Evaluate TFLite model on processed test split."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import tensorflow as tf
from sklearn.metrics import accuracy_score, classification_report, f1_score, precision_recall_fscore_support

from src.data.build_dataset import build_dataset_for_protocol
from src.data.io import dataset_exists, load_split_arrays
from src.utils.artifacts import ptq_tflite_path
from src.utils.config import apply_common_overrides, build_parser, ensure_path_dirs, load_yaml


def _quantize_input(x: np.ndarray, scale: float, zero_point: int, dtype: np.dtype) -> np.ndarray:
    q = np.round(x / scale + zero_point)
    if dtype == np.int8:
        q = np.clip(q, -128, 127)
    elif dtype == np.uint8:
        q = np.clip(q, 0, 255)
    return q.astype(dtype)


def _dequantize_output(y: np.ndarray, scale: float, zero_point: int) -> np.ndarray:
    return scale * (y.astype(np.float32) - float(zero_point))


def _run_tflite_predict(model_path: str | Path, X: np.ndarray) -> np.ndarray:
    interpreter = tf.lite.Interpreter(model_path=str(model_path))
    interpreter.allocate_tensors()

    input_info = interpreter.get_input_details()[0]
    output_info = interpreter.get_output_details()[0]

    input_dtype = input_info["dtype"]
    output_dtype = output_info["dtype"]

    input_scale, input_zp = input_info.get("quantization", (0.0, 0))
    output_scale, output_zp = output_info.get("quantization", (0.0, 0))

    preds = []
    for i in range(len(X)):
        xi = X[i : i + 1]
        if input_dtype in (np.int8, np.uint8):
            if input_scale == 0:
                raise RuntimeError("Quantized input expected but scale is zero")
            xi = _quantize_input(xi, float(input_scale), int(input_zp), input_dtype)
        else:
            xi = xi.astype(np.float32)

        interpreter.set_tensor(input_info["index"], xi)
        interpreter.invoke()
        out = interpreter.get_tensor(output_info["index"])

        if output_dtype in (np.int8, np.uint8) and output_scale != 0:
            out = _dequantize_output(out, float(output_scale), int(output_zp))

        preds.append(int(np.argmax(out, axis=1)[0]))

    return np.asarray(preds, dtype=np.int64)


def evaluate_tflite(
    cfg: dict[str, Any],
    model_path: str,
    window_size: int,
    protocol: str,
    tag: str,
) -> dict[str, Any]:
    ensure_path_dirs(cfg)
    processed_dir = cfg["paths"]["processed_dir"]
    if not dataset_exists(processed_dir, window_size, protocol):
        build_dataset_for_protocol(cfg, window_size, protocol)

    arrays = load_split_arrays(processed_dir, window_size, protocol)
    X_test, y_test = arrays["X_test"], arrays["y_test"]

    y_pred = _run_tflite_predict(model_path, X_test)
    class_names = cfg.get("classes")

    acc = float(accuracy_score(y_test, y_pred))
    macro_f1 = float(f1_score(y_test, y_pred, average="macro"))
    precision, recall, f1, support = precision_recall_fscore_support(
        y_test, y_pred, average=None, zero_division=0
    )

    per_class = {
        class_names[i]: {
            "precision": float(precision[i]),
            "recall": float(recall[i]),
            "f1": float(f1[i]),
            "support": int(support[i]),
        }
        for i in range(len(class_names))
    }

    size_kb = Path(model_path).stat().st_size / 1024.0

    metrics = {
        "tag": tag,
        "window_size": int(window_size),
        "protocol": protocol,
        "model_path": str(model_path),
        "model_size_kb": float(size_kb),
        "accuracy": acc,
        "macro_f1": macro_f1,
        "per_class": per_class,
        "classification_report": classification_report(
            y_test,
            y_pred,
            target_names=class_names,
            zero_division=0,
            output_dict=True,
        ),
    }

    reports_dir = Path(cfg["paths"]["reports_dir"])
    metrics_path = reports_dir / f"{tag}_T{window_size}_P{protocol}.json"
    report_path = reports_dir / f"{tag}_T{window_size}_P{protocol}.md"

    with metrics_path.open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    with report_path.open("w", encoding="utf-8") as f:
        f.write(f"# {tag.upper()} TFLite Evaluation (T={window_size}, protocol={protocol})\n\n")
        f.write(f"- Model: `{model_path}`\n")
        f.write(f"- Model size: {size_kb:.2f} KB\n")
        f.write(f"- Accuracy: {acc:.4f}\n")
        f.write(f"- Macro-F1: {macro_f1:.4f}\n\n")
        f.write("## Per-class metrics\n\n")
        for name in class_names:
            row = per_class[name]
            f.write(
                f"- {name}: P={row['precision']:.4f}, R={row['recall']:.4f}, F1={row['f1']:.4f}, support={row['support']}\n"
            )

    return {"metrics_json": str(metrics_path), "report_md": str(report_path), "accuracy": acc}


def main() -> None:
    parser = build_parser("Evaluate a TFLite model")
    parser.add_argument("--model", type=str, default=None, help="Path to .tflite model")
    parser.add_argument("--tag", type=str, default="ptq", help="Report tag, e.g. ptq or qat")
    args = parser.parse_args()

    cfg = apply_common_overrides(load_yaml(args.config), args)
    ws = int(cfg["window_size_default"])
    protocols = cfg.get("split_protocols", ["random_stratified"])

    for protocol in protocols:
        model_path = args.model or str(ptq_tflite_path(cfg["paths"]["models_tflite_dir"], ws, protocol))
        out = evaluate_tflite(cfg, model_path, ws, protocol, tag=args.tag)
        print(f"Evaluated TFLite model window_size={ws} protocol={protocol}")
        for k, v in out.items():
            print(f"  - {k}: {v}")


if __name__ == "__main__":
    main()
