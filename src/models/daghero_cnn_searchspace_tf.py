"""Daghero-style 1D CNN search-space templates for WISDM-first replication."""

from __future__ import annotations

import tensorflow as tf
from tensorflow.keras import layers


def build_daghero_cnn_template(
    window_size: int,
    num_features: int,
    num_classes: int,
    conv_channels: tuple[int, ...] = (32, 64),
    kernel_size: int = 7,
    pool_size: int | None = 2,
    dense_units: int = 64,
    dropout: float = 0.2,
) -> tf.keras.Model:
    """Generic Conv1D+BN template compatible with Daghero-style search.

    - 2-layer template: conv_channels length = 2
    - 4-layer template: conv_channels length = 4
    """

    inp = tf.keras.Input(shape=(window_size, num_features), name="input")
    x = inp

    for i, c in enumerate(conv_channels):
        x = layers.Conv1D(c, kernel_size, padding="same", use_bias=False, name=f"conv{i+1}")(x)
        x = layers.BatchNormalization(name=f"bn{i+1}")(x)
        x = layers.ReLU(name=f"relu{i+1}")(x)
        if pool_size is not None:
            x = layers.MaxPool1D(pool_size=pool_size, strides=pool_size, name=f"pool{i+1}")(x)

    x = layers.GlobalAveragePooling1D(name="gap")(x)
    x = layers.Dropout(dropout, name="drop")(x)
    x = layers.Dense(dense_units, activation="relu", name="fc1")(x)
    out = layers.Dense(num_classes, activation="softmax", name="classifier")(x)
    return tf.keras.Model(inp, out, name=f"daghero_cnn_{len(conv_channels)}layer")


def build_daghero_2layer(
    window_size: int,
    num_features: int,
    num_classes: int,
    channels: tuple[int, int] = (32, 64),
    kernel_size: int = 7,
    pool_size: int | None = 2,
) -> tf.keras.Model:
    return build_daghero_cnn_template(
        window_size=window_size,
        num_features=num_features,
        num_classes=num_classes,
        conv_channels=channels,
        kernel_size=kernel_size,
        pool_size=pool_size,
    )


def build_daghero_4layer(
    window_size: int,
    num_features: int,
    num_classes: int,
    channels: tuple[int, int, int, int] = (16, 32, 64, 64),
    kernel_size: int = 7,
    pool_size: int | None = 2,
) -> tf.keras.Model:
    return build_daghero_cnn_template(
        window_size=window_size,
        num_features=num_features,
        num_classes=num_classes,
        conv_channels=channels,
        kernel_size=kernel_size,
        pool_size=pool_size,
    )


def compile_daghero_cnn(model: tf.keras.Model, learning_rate: float = 1e-3) -> tf.keras.Model:
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model
