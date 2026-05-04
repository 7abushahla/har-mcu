"""Architecture-agnostic model training utilities."""

from __future__ import annotations

import time
from typing import Any, Callable

import numpy as np
import tensorflow as tf

from src.data.build_dataset import build_dataset_for_protocol
from src.data.io import dataset_exists, load_split_arrays
from src.train.augment import build_training_input
from src.utils.artifacts import model_ckpt_path, model_history_path
from src.utils.config import ensure_path_dirs
from src.utils.repro import dump_json, set_global_seed
from src.utils.runtime import check_tensorflow_runtime


CompileSpec = dict[str, Any] | Callable[[tf.keras.Model], tf.keras.Model] | None


def _compile_model(model: tf.keras.Model, compile_spec: CompileSpec) -> tf.keras.Model:
    if callable(compile_spec):
        return compile_spec(model)

    spec = compile_spec or {}
    optimizer = spec.get("optimizer", tf.keras.optimizers.Adam(learning_rate=1e-3))
    loss = spec.get("loss", "categorical_crossentropy")
    metrics = spec.get("metrics", ["accuracy"])
    model.compile(optimizer=optimizer, loss=loss, metrics=metrics)
    return model


def train_model_for_protocol(
    cfg: dict[str, Any],
    model_builder,
    compile_spec: CompileSpec,
    protocol: str,
    window_size: int,
    run_id: str,
) -> dict[str, Any]:
    """Train an arbitrary Keras model on a given WISDM protocol split."""

    ensure_path_dirs(cfg)
    check_tensorflow_runtime(cfg)
    set_global_seed(int(cfg.get("seed", 42)))

    processed_dir = cfg["paths"]["processed_dir"]
    if not dataset_exists(processed_dir, window_size, protocol):
        build_dataset_for_protocol(cfg, window_size, protocol)

    arrays = load_split_arrays(processed_dir, window_size, protocol)
    X_train, y_train = arrays["X_train"], arrays["y_train"]
    X_val, y_val = arrays["X_val"], arrays["y_val"]

    num_classes = len(cfg.get("classes", [])) or int(np.max(y_train)) + 1
    model_kwargs = dict(cfg.get("experiment", {}).get("model_kwargs", {}))
    model = model_builder(
        window_size=window_size,
        num_features=int(X_train.shape[-1]),
        num_classes=num_classes,
        **model_kwargs,
    )
    model = _compile_model(model, compile_spec)

    y_train_oh = tf.keras.utils.to_categorical(y_train, num_classes=num_classes)
    y_val_oh = tf.keras.utils.to_categorical(y_val, num_classes=num_classes)

    callbacks = [
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=float(cfg.get("train", {}).get("reduce_lr_factor", 0.5)),
            patience=int(cfg.get("train", {}).get("reduce_lr_patience", 5)),
            verbose=1,
        ),
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=int(cfg.get("train", {}).get("early_stopping_patience", 10)),
            restore_best_weights=True,
            verbose=1,
        ),
    ]

    train_input = build_training_input(
        cfg,
        X_train,
        y_train_oh,
        processed_dir=processed_dir,
        window_size=window_size,
        protocol=protocol,
        batch_size=int(cfg.get("train", {}).get("batch_size", 64)),
    )

    train_t0 = time.perf_counter()
    history = model.fit(
        *train_input.fit_args(),
        validation_data=(X_val, y_val_oh),
        epochs=int(cfg.get("train", {}).get("epochs", 50)),
        callbacks=callbacks,
        verbose=2,
        **train_input.fit_kwargs,
    )
    training_time_sec = float(time.perf_counter() - train_t0)

    model_name = str(cfg.get("experiment", {}).get("model_variant", model.name))
    ckpt = model_ckpt_path(
        cfg["paths"]["checkpoints_dir"],
        model_name=model_name,
        window_size=window_size,
        protocol=protocol,
        run_id=run_id,
    )
    hist_path = model_history_path(
        cfg["paths"]["checkpoints_dir"],
        model_name=model_name,
        window_size=window_size,
        protocol=protocol,
        run_id=run_id,
    )
    ckpt.parent.mkdir(parents=True, exist_ok=True)
    model.save(ckpt)
    dump_json(hist_path, history.history)
    checkpoint_size_kb = float(ckpt.stat().st_size / 1024.0) if ckpt.exists() else None

    return {
        "model_name": model_name,
        "run_id": run_id,
        "checkpoint": str(ckpt),
        "checkpoint_size_kb": checkpoint_size_kb,
        "history": str(hist_path),
        "history_json": str(hist_path),
        "epochs_ran": int(len(history.history.get("loss", []))),
        "final_val_accuracy": float(history.history.get("val_accuracy", [0.0])[-1]),
        "training_time_sec": training_time_sec,
    }
