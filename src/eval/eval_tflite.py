"""Evaluate TFLite model on processed test split."""

from __future__ import annotations

import argparse
import time
from pathlib import Path
from typing import Any

import numpy as np
import tensorflow as tf
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
)

from src.data.build_dataset import build_dataset_for_protocol
from src.data.io import dataset_exists, load_split_arrays
from src.eval.plots import save_confusion_matrix_plot
from src.utils.artifacts import tflite_confusion_png
from src.utils.artifacts import ptq_tflite_path
from src.utils.config import apply_common_overrides, build_parser, ensure_path_dirs, load_yaml
from src.utils.repro import dump_json


def _quantize_input(x: np.ndarray, scale: float, zero_point: int, dtype: np.dtype) -> np.ndarray:
    q = np.round(x / scale + zero_point)
    if dtype == np.int8:
        q = np.clip(q, -128, 127)
    elif dtype == np.uint8:
        q = np.clip(q, 0, 255)
    return q.astype(dtype)


def _dequantize_output(y: np.ndarray, scale: float, zero_point: int) -> np.ndarray:
    return scale * (y.astype(np.float32) - float(zero_point))


def _build_tflite_interpreter(model_path: str | Path) -> tf.lite.Interpreter:
    return tf.lite.Interpreter(
        model_path=str(model_path),
        experimental_op_resolver_type=tf.lite.experimental.OpResolverType.BUILTIN_WITHOUT_DEFAULT_DELEGATES,
        experimental_delegates=[],
        num_threads=1,
    )


def _interpreter_ops(interpreter: tf.lite.Interpreter) -> list[str]:
    if not hasattr(interpreter, "_get_ops_details"):
        return []
    details = interpreter._get_ops_details()  # pylint: disable=protected-access
    return sorted({str(d.get("op_name", "UNKNOWN")) for d in details})


def _run_tflite_predict(model_path: str | Path, X: np.ndarray) -> tuple[np.ndarray, str, str, list[str]]:
    interpreter = _build_tflite_interpreter(model_path)
    interpreter.allocate_tensors()
    ops = _interpreter_ops(interpreter)

    input_info = interpreter.get_input_details()[0]
    output_info = interpreter.get_output_details()[0]

    input_dtype = input_info["dtype"]
    output_dtype = output_info["dtype"]

    input_scale, input_zp = input_info.get("quantization", (0.0, 0))
    output_scale, output_zp = output_info.get("quantization", (0.0, 0))

    preds: list[int] = []
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

    return np.asarray(preds, dtype=np.int64), str(input_dtype), str(output_dtype), ops


def _summarize_latency_ms(latencies_ms: list[float]) -> dict[str, float | None]:
    if not latencies_ms:
        return {
            "inference_latency_ms_median": None,
            "inference_latency_ms_p95": None,
            "inference_latency_ms_mean": None,
        }
    arr = np.asarray(latencies_ms, dtype=np.float64)
    return {
        "inference_latency_ms_median": float(np.median(arr)),
        "inference_latency_ms_p95": float(np.percentile(arr, 95)),
        "inference_latency_ms_mean": float(np.mean(arr)),
    }


def _measure_tflite_latency_ms(
    model_path: str | Path,
    X: np.ndarray,
    *,
    warmup_samples: int,
    timed_samples: int,
) -> dict[str, float | int | None]:
    interpreter = _build_tflite_interpreter(model_path)
    interpreter.allocate_tensors()
    input_info = interpreter.get_input_details()[0]
    output_info = interpreter.get_output_details()[0]
    input_dtype = input_info["dtype"]

    input_scale, input_zp = input_info.get("quantization", (0.0, 0))
    output_scale, output_zp = output_info.get("quantization", (0.0, 0))
    output_dtype = output_info["dtype"]

    n_total = len(X)
    warmup_n = min(max(0, int(warmup_samples)), n_total)
    timed_n = min(max(0, int(timed_samples)), max(0, n_total - warmup_n))

    def _run_one(idx: int, *, timed: bool) -> float | None:
        xi = X[idx : idx + 1]
        if input_dtype in (np.int8, np.uint8):
            if input_scale == 0:
                raise RuntimeError("Quantized input expected but scale is zero")
            xi = _quantize_input(xi, float(input_scale), int(input_zp), input_dtype)
        else:
            xi = xi.astype(np.float32)

        interpreter.set_tensor(input_info["index"], xi)
        if timed:
            t0 = time.perf_counter()
            interpreter.invoke()
            dt_ms = (time.perf_counter() - t0) * 1000.0
        else:
            interpreter.invoke()
            dt_ms = None
        out = interpreter.get_tensor(output_info["index"])
        if output_dtype in (np.int8, np.uint8) and output_scale != 0:
            _dequantize_output(out, float(output_scale), int(output_zp))
        return dt_ms

    for i in range(warmup_n):
        _run_one(i, timed=False)

    latencies: list[float] = []
    for i in range(warmup_n, warmup_n + timed_n):
        dt_ms = _run_one(i, timed=True)
        if dt_ms is not None:
            latencies.append(float(dt_ms))

    summary = _summarize_latency_ms(latencies)
    summary["warmup_samples"] = int(warmup_n)
    summary["timed_samples"] = int(timed_n)
    return summary


def evaluate_tflite(
    cfg: dict[str, Any],
    model_path: str,
    window_size: int,
    protocol: str,
    tag: str,
    reports_dir_override: str | Path | None = None,
) -> dict[str, Any]:
    ensure_path_dirs(cfg)
    processed_dir = cfg["paths"]["processed_dir"]
    if not dataset_exists(processed_dir, window_size, protocol):
        build_dataset_for_protocol(cfg, window_size, protocol)

    arrays = load_split_arrays(processed_dir, window_size, protocol)
    X_test, y_test = arrays["X_test"], arrays["y_test"]

    y_pred, input_dtype, output_dtype, interpreter_ops = _run_tflite_predict(model_path, X_test)
    class_names = cfg.get("classes")
    labels = list(range(len(class_names)))

    acc = float(accuracy_score(y_test, y_pred))
    macro_f1 = float(f1_score(y_test, y_pred, average="macro"))
    precision, recall, f1, support = precision_recall_fscore_support(
        y_test, y_pred, labels=labels, average=None, zero_division=0
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
    cm = confusion_matrix(y_test, y_pred, labels=labels)

    size_kb = Path(model_path).stat().st_size / 1024.0
    reports_dir = Path(reports_dir_override) if reports_dir_override else Path(cfg["paths"]["reports_dir"])
    reports_dir.mkdir(parents=True, exist_ok=True)
    confusion_plot = tflite_confusion_png(reports_dir, tag, window_size, protocol)
    cmap = "Oranges" if "ptq" in tag.lower() else "Greens" if "qat" in tag.lower() else "Blues"
    save_confusion_matrix_plot(
        cm,
        class_names=class_names,
        out_png=confusion_plot,
        title=f"{tag.upper()} Confusion Matrix ({protocol}, T={window_size})",
        cmap=cmap,
    )

    timing_cfg = cfg.get("eval", {}).get("tflite_timing", {})
    if bool(timing_cfg.get("enabled", True)):
        latency = _measure_tflite_latency_ms(
            model_path=model_path,
            X=X_test,
            warmup_samples=int(timing_cfg.get("warmup_samples", 32)),
            timed_samples=int(timing_cfg.get("timed_samples", 256)),
        )
    else:
        latency = {
            "inference_latency_ms_median": None,
            "inference_latency_ms_p95": None,
            "inference_latency_ms_mean": None,
            "warmup_samples": 0,
            "timed_samples": 0,
        }

    metrics = {
        "tag": tag,
        "window_size": int(window_size),
        "protocol": protocol,
        "model_path": str(model_path),
        "model_size_kb": float(size_kb),
        "input_dtype": input_dtype,
        "output_dtype": output_dtype,
        "interpreter_ops": interpreter_ops,
        "interpreter_op_count": int(len(interpreter_ops)),
        "accuracy": acc,
        "macro_f1": macro_f1,
        "confusion_matrix": cm.tolist(),
        "confusion_plot": str(confusion_plot),
        "per_class": per_class,
        "classification_report": classification_report(
            y_test,
            y_pred,
            labels=labels,
            target_names=class_names,
            zero_division=0,
            output_dict=True,
        ),
        **latency,
    }

    metrics_path = reports_dir / f"{tag}_T{window_size}_P{protocol}.json"
    report_path = reports_dir / f"{tag}_T{window_size}_P{protocol}.md"

    dump_json(metrics_path, metrics)

    with report_path.open("w", encoding="utf-8") as f:
        f.write(f"# {tag.upper()} TFLite Evaluation (T={window_size}, protocol={protocol})\n\n")
        f.write(f"- Model: `{model_path}`\n")
        f.write(f"- Model size: {size_kb:.2f} KB\n")
        f.write(f"- Accuracy: {acc:.4f}\n")
        f.write(f"- Macro-F1: {macro_f1:.4f}\n\n")
        f.write(f"- Input dtype: `{input_dtype}`\n")
        f.write(f"- Output dtype: `{output_dtype}`\n")
        f.write(f"- Interpreter op count: {metrics['interpreter_op_count']}\n")
        f.write(f"- Interpreter ops: `{metrics['interpreter_ops']}`\n")
        if metrics.get("inference_latency_ms_median") is not None:
            f.write(f"- Inference latency median: {metrics['inference_latency_ms_median']:.3f} ms/sample\n")
            f.write(f"- Inference latency p95: {metrics['inference_latency_ms_p95']:.3f} ms/sample\n")
            f.write(f"- Timed samples: {metrics['timed_samples']}\n")
            f.write(f"- Warmup samples: {metrics['warmup_samples']}\n")
        f.write(f"- Confusion matrix plot: `{confusion_plot}`\n\n")
        f.write("## Per-class metrics\n\n")
        for name in class_names:
            row = per_class[name]
            f.write(
                f"- {name}: P={row['precision']:.4f}, R={row['recall']:.4f}, F1={row['f1']:.4f}, support={row['support']}\n"
            )

    return {
        "metrics_json": str(metrics_path),
        "report_md": str(report_path),
        "accuracy": acc,
        "macro_f1": macro_f1,
        "confusion_plot": str(confusion_plot),
    }


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
