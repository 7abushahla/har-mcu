"""Evaluate baseline Keras model on test split."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
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
from src.train.train_baseline import train_baseline_for_protocol
from src.utils.artifacts import (
    baseline_ckpt_path,
    baseline_metrics_json,
    baseline_report_md,
    confusion_png,
)
from src.utils.config import apply_common_overrides, build_parser, ensure_path_dirs, load_yaml


def evaluate_baseline_for_protocol(
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
    X_test, y_test = arrays["X_test"], arrays["y_test"]

    model = tf.keras.models.load_model(ckpt_path)
    probs = model.predict(X_test, verbose=0)
    y_pred = probs.argmax(axis=1)

    class_names = cfg.get("classes")
    acc = float(accuracy_score(y_test, y_pred))
    macro_f1 = float(f1_score(y_test, y_pred, average="macro"))
    precision, recall, f1, support = precision_recall_fscore_support(
        y_test, y_pred, average=None, zero_division=0
    )

    cm = confusion_matrix(y_test, y_pred)

    png_path = confusion_png(cfg["paths"]["reports_dir"], window_size, protocol, suffix="baseline")
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False)
    plt.title(f"Baseline Confusion Matrix ({protocol}, T={window_size})")
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.tight_layout()
    png_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(png_path)
    plt.close()

    per_class = {
        class_names[i]: {
            "precision": float(precision[i]),
            "recall": float(recall[i]),
            "f1": float(f1[i]),
            "support": int(support[i]),
        }
        for i in range(len(class_names))
    }

    metrics = {
        "window_size": int(window_size),
        "protocol": protocol,
        "accuracy": acc,
        "macro_f1": macro_f1,
        "per_class": per_class,
        "confusion_matrix": cm.tolist(),
        "confusion_plot": str(png_path),
        "classification_report": classification_report(
            y_test,
            y_pred,
            target_names=class_names,
            zero_division=0,
            output_dict=True,
        ),
    }

    metrics_path = baseline_metrics_json(cfg["paths"]["reports_dir"], window_size, protocol)
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    with metrics_path.open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    md_path = baseline_report_md(cfg["paths"]["reports_dir"], window_size, protocol)
    with md_path.open("w", encoding="utf-8") as f:
        f.write(f"# Baseline Evaluation (T={window_size}, protocol={protocol})\n\n")
        f.write(f"- Accuracy: {acc:.4f}\n")
        f.write(f"- Macro-F1: {macro_f1:.4f}\n")
        f.write(f"- Confusion matrix plot: `{png_path}`\n\n")
        f.write("## Per-class metrics\n\n")
        for name in class_names:
            row = per_class[name]
            f.write(
                f"- {name}: P={row['precision']:.4f}, R={row['recall']:.4f}, F1={row['f1']:.4f}, support={row['support']}\n"
            )

    return {
        "metrics_json": str(metrics_path),
        "report_md": str(md_path),
        "accuracy": acc,
        "macro_f1": macro_f1,
    }


def main() -> None:
    parser = build_parser("Evaluate baseline model")
    args = parser.parse_args()
    cfg = apply_common_overrides(load_yaml(args.config), args)
    ws = int(cfg["window_size_default"])

    for protocol in cfg.get("split_protocols", ["random_stratified"]):
        out = evaluate_baseline_for_protocol(cfg, ws, protocol)
        print(f"Evaluated baseline window_size={ws} protocol={protocol}")
        for k, v in out.items():
            print(f"  - {k}: {v}")


if __name__ == "__main__":
    main()
