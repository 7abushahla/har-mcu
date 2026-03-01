"""Train embedding variant for TinyOL simulation."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np
import tensorflow as tf

from src.data.build_dataset import build_dataset_for_protocol
from src.data.io import dataset_exists, load_split_arrays
from src.models.deepconv_lstm_embed import build_deepconv_lstm_embed
from src.utils.artifacts import dataset_prefix
from src.utils.config import apply_common_overrides, build_parser, ensure_path_dirs, load_yaml
from src.utils.repro import set_global_seed
from src.utils.runtime import check_tensorflow_runtime


def train_embed_for_protocol(
    cfg: dict[str, Any],
    window_size: int,
    protocol: str,
    embedding_dim: int = 128,
) -> dict[str, str]:
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
    y_train_oh = tf.keras.utils.to_categorical(y_train, num_classes)
    y_val_oh = tf.keras.utils.to_categorical(y_val, num_classes)

    cls_model, embed_model = build_deepconv_lstm_embed(
        window_size=window_size,
        num_features=int(X_train.shape[-1]),
        num_classes=num_classes,
        embedding_dim=embedding_dim,
        dropout=float(cfg["train"]["dropout"]),
    )

    cls_model.compile(
        optimizer=tf.keras.optimizers.RMSprop(learning_rate=float(cfg["train"]["learning_rate"])),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    cls_model.fit(
        X_train,
        y_train_oh,
        validation_data=(X_val, y_val_oh),
        epochs=int(cfg["train"]["epochs"]),
        batch_size=int(cfg["train"]["batch_size"]),
        verbose=2,
    )

    tag = dataset_prefix(window_size, protocol)
    ckpt_dir = Path(cfg["paths"]["checkpoints_dir"])
    ckpt_dir.mkdir(parents=True, exist_ok=True)

    cls_path = ckpt_dir / f"deepconv_lstm_embed_cls_{tag}.keras"
    emb_path = ckpt_dir / f"deepconv_lstm_embed_{tag}.keras"
    cls_model.save(cls_path)
    embed_model.save(emb_path)
    return {"classifier": str(cls_path), "embedding": str(emb_path)}


def main() -> None:
    parser = build_parser("Train embedding model for TinyOL")
    parser.add_argument("--embedding-dim", type=int, default=128)
    args = parser.parse_args()

    cfg = apply_common_overrides(load_yaml(args.config), args)
    ws = int(cfg["window_size_default"])

    for protocol in cfg.get("split_protocols", ["random_stratified"]):
        out = train_embed_for_protocol(cfg, ws, protocol, embedding_dim=args.embedding_dim)
        print(f"Trained embedding model window_size={ws} protocol={protocol}")
        for k, v in out.items():
            print(f"  - {k}: {v}")


if __name__ == "__main__":
    main()
