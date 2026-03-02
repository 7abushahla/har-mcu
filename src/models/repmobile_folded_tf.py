"""RepMobile-style folded inference architecture (plain single-branch)."""

from __future__ import annotations

import tensorflow as tf
from tensorflow.keras import layers


def _repmobile_folded_block(
    x: tf.Tensor,
    out_channels: int,
    stride: int,
    dropout: float,
    name: str,
) -> tf.Tensor:
    """Single-branch depthwise-separable block used at inference time."""

    inp = x
    x = layers.SeparableConv1D(
        out_channels,
        kernel_size=3,
        strides=stride,
        padding="same",
        use_bias=False,
        name=f"{name}_sepconv",
    )(x)
    x = layers.BatchNormalization(name=f"{name}_bn")(x)
    x = layers.ReLU(name=f"{name}_relu")(x)
    x = layers.Dropout(dropout, name=f"{name}_drop")(x)

    if stride == 1 and int(inp.shape[-1]) == out_channels:
        x = layers.Add(name=f"{name}_residual")([inp, x])
    return x


def build_repmobile_folded(
    window_size: int,
    num_features: int,
    num_classes: int,
    channels: tuple[int, int, int, int] = (32, 64, 96, 128),
    stride: int = 1,
    dropout: float = 0.1,
) -> tf.keras.Model:
    """Build folded RepMobile equivalent for PTQ/QAT export."""

    inp = tf.keras.Input(shape=(window_size, num_features), name="input")
    x = inp
    for i, c in enumerate(channels):
        block_stride = stride if i == 0 else 1
        x = _repmobile_folded_block(x, c, block_stride, dropout, name=f"repblock_{i}")

    x = layers.GlobalAveragePooling1D(name="gap")(x)
    x = layers.Dropout(dropout, name="head_drop")(x)
    out = layers.Dense(num_classes, activation="softmax", name="classifier")(x)
    return tf.keras.Model(inp, out, name="repmobile_folded")


def compile_repmobile_folded(model: tf.keras.Model, learning_rate: float = 1e-4) -> tf.keras.Model:
    model.compile(
        optimizer=tf.keras.optimizers.SGD(learning_rate=learning_rate, momentum=0.9),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model
