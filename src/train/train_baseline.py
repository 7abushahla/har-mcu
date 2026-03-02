"""Train baseline DeepConv+LSTM model."""

from __future__ import annotations

from typing import Any

import numpy as np
import tensorflow as tf

from src.data.build_dataset import build_dataset_for_protocol
from src.data.io import dataset_exists, load_split_arrays
from src.models.deepconv_lstm import build_deepconv_lstm, build_deepconv_lstm_conv2d, compile_deepconv_lstm
from src.utils.artifacts import baseline_ckpt_path, history_path
from src.utils.config import apply_common_overrides, build_parser, ensure_path_dirs, load_yaml
from src.utils.repro import dump_json, set_global_seed
from src.utils.runtime import check_tensorflow_runtime


def _to_one_hot(y: np.ndarray, num_classes: int) -> np.ndarray:
    return tf.keras.utils.to_categorical(y, num_classes=num_classes)


def train_baseline_for_protocol(
    cfg: dict[str, Any],
    window_size: int,
    protocol: str,
    model_builder=None,
) -> dict[str, Any]:
    """Train (or reload) one fp32 baseline model for the given protocol.

    Args:
        cfg: effective config dict.
        window_size: number of timesteps per window.
        protocol: split protocol name (e.g. ``"random_stratified"``).
        model_builder: callable with signature
            ``(window_size, num_features, num_classes, dropout) -> tf.keras.Model``.
            Defaults to :func:`build_deepconv_lstm` (Conv1D architecture).
            Pass :func:`build_deepconv_lstm_conv2d` for the QAT-compatible
            Conv2D equivalent.
    """
    ensure_path_dirs(cfg)
    check_tensorflow_runtime(cfg)
    set_global_seed(int(cfg["seed"]))

    processed_dir = cfg["paths"]["processed_dir"]
    if not dataset_exists(processed_dir, window_size, protocol):
        build_dataset_for_protocol(cfg, window_size, protocol)

    arrays = load_split_arrays(processed_dir, window_size, protocol)
    X_train, y_train = arrays["X_train"], arrays["y_train"]
    X_val, y_val = arrays["X_val"], arrays["y_val"]

    num_classes = len(cfg.get("classes", [])) or int(np.max(y_train)) + 1
    y_train_oh = _to_one_hot(y_train, num_classes)
    y_val_oh = _to_one_hot(y_val, num_classes)

    _builder = model_builder if model_builder is not None else build_deepconv_lstm
    model = _builder(
        window_size=window_size,
        num_features=int(X_train.shape[-1]),
        num_classes=num_classes,
        dropout=float(cfg["train"]["dropout"]),
    )
    compile_deepconv_lstm(model, learning_rate=float(cfg["train"]["learning_rate"]))

    callbacks = [
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=float(cfg["train"]["reduce_lr_factor"]),
            patience=int(cfg["train"]["reduce_lr_patience"]),
            verbose=1,
        ),
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=int(cfg["train"]["early_stopping_patience"]),
            restore_best_weights=True,
            verbose=1,
        ),
    ]

    history = model.fit(
        X_train,
        y_train_oh,
        validation_data=(X_val, y_val_oh),
        epochs=int(cfg["train"]["epochs"]),
        batch_size=int(cfg["train"]["batch_size"]),
        callbacks=callbacks,
        verbose=2,
    )

    ckpt_path = baseline_ckpt_path(cfg["paths"]["checkpoints_dir"], window_size, protocol)
    ckpt_path.parent.mkdir(parents=True, exist_ok=True)
    model.save(ckpt_path)

    hist_path = history_path(cfg["paths"]["checkpoints_dir"], window_size, protocol)
    dump_json(hist_path, history.history)

    out = {
        "checkpoint": str(ckpt_path),
        "history": str(hist_path),
        "epochs_ran": int(len(history.history.get("loss", []))),
        "final_val_accuracy": float(history.history.get("val_accuracy", [0.0])[-1]),
    }
    return out


def main() -> None:
    parser = build_parser("Train baseline DeepConv+LSTM")
    args = parser.parse_args()
    cfg = apply_common_overrides(load_yaml(args.config), args)

    protocols = cfg.get("split_protocols", ["random_stratified"])
    ws = int(cfg["window_size_default"])
    for protocol in protocols:
        out = train_baseline_for_protocol(cfg, ws, protocol)
        print(f"Trained baseline window_size={ws} protocol={protocol}")
        for k, v in out.items():
            print(f"  - {k}: {v}")


if __name__ == "__main__":
    main()
