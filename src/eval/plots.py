"""Shared plotting helpers for evaluation and reporting."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np


def save_training_curves(
    history_dict_or_json: dict[str, Any] | str | Path,
    out_png: str | Path,
    *,
    title: str,
    train_acc_keys: tuple[str, ...] = ("accuracy", "acc"),
    val_acc_keys: tuple[str, ...] = ("val_accuracy", "val_acc"),
) -> str | None:
    if isinstance(history_dict_or_json, (str, Path)):
        import json

        with Path(history_dict_or_json).open("r", encoding="utf-8") as f:
            history = json.load(f)
    else:
        history = history_dict_or_json

    if not isinstance(history, dict) or "loss" not in history:
        return None

    def _pick(keys: tuple[str, ...]) -> list[float]:
        for key in keys:
            if key in history:
                return list(history[key])
        return []

    train_loss = list(history.get("loss", []))
    val_loss = list(history.get("val_loss", []))
    train_acc = _pick(train_acc_keys)
    val_acc = _pick(val_acc_keys)

    if not train_loss:
        return None

    out_path = Path(out_png)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    epochs = np.arange(1, len(train_loss) + 1)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
    axes[0].plot(epochs, train_loss, label="train")
    if val_loss:
        axes[0].plot(epochs, val_loss, label="val")
    axes[0].set_title("Loss")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Loss")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    if train_acc:
        axes[1].plot(epochs, train_acc, label="train")
    if val_acc:
        axes[1].plot(epochs, val_acc, label="val")
    axes[1].set_title("Accuracy")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("Accuracy")
    axes[1].grid(True, alpha=0.3)
    if train_acc or val_acc:
        axes[1].legend()

    fig.suptitle(title)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)
    return str(out_path)


def save_confusion_matrix_plot(
    confusion_matrix: np.ndarray | list[list[int]],
    class_names: list[str],
    out_png: str | Path,
    *,
    title: str,
    cmap: str = "Blues",
) -> str:
    cm = np.asarray(confusion_matrix)
    out_path = Path(out_png)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(cm, cmap=cmap)
    ax.set_title(title)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("True")
    ax.set_xticks(np.arange(len(class_names)))
    ax.set_yticks(np.arange(len(class_names)))
    ax.set_xticklabels(class_names, rotation=45, ha="right")
    ax.set_yticklabels(class_names)

    thresh = cm.max() / 2.0 if cm.size else 0
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(
                j,
                i,
                str(int(cm[i, j])),
                ha="center",
                va="center",
                color="white" if cm[i, j] > thresh else "black",
                fontsize=9,
            )

    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)
    return str(out_path)
