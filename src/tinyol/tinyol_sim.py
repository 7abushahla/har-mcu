"""TinyOL-style online head adaptation simulator."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from sklearn.metrics import accuracy_score, f1_score

from src.data.build_dataset import build_dataset_for_protocol
from src.data.io import dataset_exists, load_split_arrays
from src.train.train_embed import train_embed_for_protocol
from src.utils.artifacts import dataset_prefix
from src.utils.config import apply_common_overrides, build_parser, ensure_path_dirs, load_yaml
from src.utils.repro import set_global_seed


def softmax(logits: np.ndarray) -> np.ndarray:
    z = logits - logits.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)


def predict_logits(X: np.ndarray, W: np.ndarray, b: np.ndarray) -> np.ndarray:
    return X @ W.T + b[None, :]


def train_head_offline(X: np.ndarray, y: np.ndarray, num_classes: int, lr: float, epochs: int) -> tuple[np.ndarray, np.ndarray]:
    W = np.zeros((num_classes, X.shape[1]), dtype=np.float32)
    b = np.zeros((num_classes,), dtype=np.float32)
    y_one_hot = tf.keras.utils.to_categorical(y, num_classes=num_classes).astype(np.float32)

    for _ in range(epochs):
        logits = predict_logits(X, W, b)
        probs = softmax(logits)
        grad_logits = (probs - y_one_hot) / max(len(X), 1)

        dW = grad_logits.T @ X
        db = grad_logits.sum(axis=0)

        W -= lr * dW
        b -= lr * db

    return W, b


def online_update(W: np.ndarray, b: np.ndarray, x: np.ndarray, y: int, lr: float) -> tuple[np.ndarray, np.ndarray]:
    logits = (x[None, :] @ W.T) + b[None, :]
    probs = softmax(logits).reshape(-1)
    grad = probs
    grad[y] -= 1.0

    W = W - lr * np.outer(grad, x)
    b = b - lr * grad
    return W, b


def apply_domain_shift(X: np.ndarray, seed: int = 42) -> np.ndarray:
    rng = np.random.default_rng(seed)
    scale = rng.uniform(0.85, 1.15, size=(1, 1, X.shape[-1])).astype(np.float32)
    bias = rng.uniform(-0.2, 0.2, size=(1, 1, X.shape[-1])).astype(np.float32)
    noise = rng.normal(0.0, 0.05, size=X.shape).astype(np.float32)
    return (X * scale + bias + noise).astype(np.float32)


def run_tinyol_sim(
    cfg: dict[str, Any],
    window_size: int,
    protocol: str,
    k_labels: int = 100,
    online_lr: float = 0.01,
) -> dict[str, Any]:
    ensure_path_dirs(cfg)
    set_global_seed(int(cfg["seed"]))

    processed_dir = cfg["paths"]["processed_dir"]
    if not dataset_exists(processed_dir, window_size, protocol):
        build_dataset_for_protocol(cfg, window_size, protocol)

    tag = dataset_prefix(window_size, protocol)
    emb_path = Path(cfg["paths"]["checkpoints_dir"]) / f"deepconv_lstm_embed_{tag}.keras"
    if not emb_path.exists():
        train_embed_for_protocol(cfg, window_size, protocol, embedding_dim=128)

    arrays = load_split_arrays(processed_dir, window_size, protocol)
    X_train, y_train = arrays["X_train"], arrays["y_train"]
    X_test, y_test = arrays["X_test"], arrays["y_test"]

    X_test_shifted = apply_domain_shift(X_test, seed=int(cfg["seed"]))

    embed_model = tf.keras.models.load_model(emb_path)
    E_train = embed_model.predict(X_train, verbose=0)
    E_test_shifted = embed_model.predict(X_test_shifted, verbose=0)

    num_classes = len(cfg.get("classes", [])) or int(np.max(y_train)) + 1
    W, b = train_head_offline(E_train, y_train, num_classes=num_classes, lr=0.05, epochs=200)

    rng = np.random.default_rng(int(cfg["seed"]))
    idx = np.arange(len(E_test_shifted))
    rng.shuffle(idx)
    E_test_shifted = E_test_shifted[idx]
    y_test_shuffled = y_test[idx]

    k = min(int(k_labels), len(E_test_shifted) // 2)
    E_adapt, y_adapt = E_test_shifted[:k], y_test_shuffled[:k]
    E_eval, y_eval = E_test_shifted[k:], y_test_shuffled[k:]

    pred_before = np.argmax(predict_logits(E_eval, W, b), axis=1)
    acc_before = float(accuracy_score(y_eval, pred_before))
    f1_before = float(f1_score(y_eval, pred_before, average="macro"))

    curve_acc = [acc_before]
    curve_f1 = [f1_before]

    for i in range(len(E_adapt)):
        W, b = online_update(W, b, E_adapt[i], int(y_adapt[i]), lr=float(online_lr))
        pred_cur = np.argmax(predict_logits(E_eval, W, b), axis=1)
        curve_acc.append(float(accuracy_score(y_eval, pred_cur)))
        curve_f1.append(float(f1_score(y_eval, pred_cur, average="macro")))

    pred_after = np.argmax(predict_logits(E_eval, W, b), axis=1)
    acc_after = float(accuracy_score(y_eval, pred_after))
    f1_after = float(f1_score(y_eval, pred_after, average="macro"))

    reports_dir = Path(cfg["paths"]["reports_dir"])
    reports_dir.mkdir(parents=True, exist_ok=True)

    curve_png = reports_dir / f"tinyol_curve_T{window_size}_P{protocol}.png"
    plt.figure(figsize=(8, 5))
    plt.plot(curve_acc, label="Accuracy")
    plt.plot(curve_f1, label="Macro-F1")
    plt.xlabel("Online updates")
    plt.ylabel("Score")
    plt.title(f"TinyOL Adaptation Curve (T={window_size}, {protocol})")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(curve_png)
    plt.close()

    payload = {
        "window_size": int(window_size),
        "protocol": protocol,
        "k_labels": int(k),
        "online_lr": float(online_lr),
        "accuracy_before": acc_before,
        "accuracy_after": acc_after,
        "macro_f1_before": f1_before,
        "macro_f1_after": f1_after,
        "curve_png": str(curve_png),
    }

    json_path = reports_dir / f"tinyol_ablation_T{window_size}_P{protocol}.json"
    md_path = reports_dir / "tinyol_ablation.md"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    with md_path.open("a", encoding="utf-8") as f:
        f.write(f"## TinyOL Ablation (T={window_size}, protocol={protocol})\n\n")
        f.write(f"- Labeled adaptation windows K: {k}\n")
        f.write(f"- Accuracy before adaptation: {acc_before:.4f}\n")
        f.write(f"- Accuracy after adaptation: {acc_after:.4f}\n")
        f.write(f"- Macro-F1 before adaptation: {f1_before:.4f}\n")
        f.write(f"- Macro-F1 after adaptation: {f1_after:.4f}\n")
        f.write(f"- Curve plot: `{curve_png}`\n\n")

    return {"report_json": str(json_path), "report_md": str(md_path)}


def main() -> None:
    parser = build_parser("Run TinyOL online-learning simulation")
    parser.add_argument("--k-labels", type=int, default=100)
    parser.add_argument("--online-lr", type=float, default=0.01)
    args = parser.parse_args()

    cfg = apply_common_overrides(load_yaml(args.config), args)
    ws = int(cfg["window_size_default"])

    for protocol in cfg.get("split_protocols", ["random_stratified"]):
        out = run_tinyol_sim(cfg, ws, protocol, k_labels=args.k_labels, online_lr=args.online_lr)
        print(f"TinyOL sim done window_size={ws} protocol={protocol}")
        for k, v in out.items():
            print(f"  - {k}: {v}")


if __name__ == "__main__":
    main()
