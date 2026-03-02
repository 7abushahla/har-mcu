"""Architecture-agnostic model evaluation utilities."""

from __future__ import annotations

from pathlib import Path
from typing import Any

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
from src.utils.artifacts import model_confusion_png, model_metrics_json, model_report_md
from src.utils.config import ensure_path_dirs
from src.utils.repro import dump_json


def evaluate_model_for_protocol(
    cfg: dict[str, Any],
    model_path: str,
    protocol: str,
    window_size: int,
    run_id: str,
    reports_dir_override: str | Path | None = None,
) -> dict[str, Any]:
    """Evaluate a saved Keras model checkpoint on test split."""

    ensure_path_dirs(cfg)
    processed_dir = cfg["paths"]["processed_dir"]
    if not dataset_exists(processed_dir, window_size, protocol):
        build_dataset_for_protocol(cfg, window_size, protocol)

    arrays = load_split_arrays(processed_dir, window_size, protocol)
    X_test, y_test = arrays["X_test"], arrays["y_test"]

    model = tf.keras.models.load_model(model_path)
    probs = model.predict(X_test, verbose=0)
    y_pred = probs.argmax(axis=1)

    class_names = cfg.get("classes")
    acc = float(accuracy_score(y_test, y_pred))
    macro_f1 = float(f1_score(y_test, y_pred, average="macro"))
    precision, recall, f1, support = precision_recall_fscore_support(
        y_test, y_pred, average=None, zero_division=0
    )

    cm = confusion_matrix(y_test, y_pred)

    reports_dir = Path(reports_dir_override) if reports_dir_override else Path(cfg["paths"]["reports_dir"])
    model_name = str(cfg.get("experiment", {}).get("model_variant", Path(model_path).stem))
    png_path = model_confusion_png(
        reports_dir,
        model_name=model_name,
        window_size=window_size,
        protocol=protocol,
        run_id=run_id,
    )
    save_confusion_matrix_plot(
        cm,
        class_names=class_names,
        out_png=png_path,
        title=f"{model_name} FP32 Confusion Matrix ({protocol}, T={window_size})",
        cmap="Blues",
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

    metrics = {
        "paper_slug": cfg.get("experiment", {}).get("paper_slug"),
        "model_name": model_name,
        "run_id": run_id,
        "window_size": int(window_size),
        "protocol": protocol,
        "seed": int(cfg.get("seed", 42)),
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

    metrics_path = model_metrics_json(
        reports_dir,
        model_name=model_name,
        window_size=window_size,
        protocol=protocol,
        run_id=run_id,
    )
    dump_json(metrics_path, metrics)

    report_path = model_report_md(
        reports_dir,
        model_name=model_name,
        window_size=window_size,
        protocol=protocol,
        run_id=run_id,
    )
    with report_path.open("w", encoding="utf-8") as f:
        f.write(f"# {model_name} Evaluation (T={window_size}, protocol={protocol}, run={run_id})\n\n")
        f.write(f"- Accuracy: {acc:.4f}\n")
        f.write(f"- Macro-F1: {macro_f1:.4f}\n")
        f.write(f"- Confusion matrix: `{png_path}`\n")

    return {
        "metrics_json": str(metrics_path),
        "report_md": str(report_path),
        "accuracy": acc,
        "macro_f1": macro_f1,
        "model_name": model_name,
        "run_id": run_id,
    }
