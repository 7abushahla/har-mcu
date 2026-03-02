"""XTinyHAR-style inertial transformer student for WISDM-first replication."""

from __future__ import annotations

import tensorflow as tf
from tensorflow.keras import layers


@tf.keras.utils.register_keras_serializable(package="har_mcu")
class TransformerEncoderBlock(layers.Layer):
    """Minimal pre-norm transformer encoder block."""

    def __init__(
        self,
        embed_dim: int,
        num_heads: int,
        mlp_ratio: float = 2.0,
        dropout: float = 0.1,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.embed_dim = int(embed_dim)
        self.num_heads = int(num_heads)
        self.mlp_ratio = float(mlp_ratio)
        self.dropout = float(dropout)
        self.norm1 = layers.LayerNormalization(epsilon=1e-6)
        self.attn = layers.MultiHeadAttention(
            num_heads=self.num_heads,
            key_dim=max(1, self.embed_dim // max(1, self.num_heads)),
            dropout=self.dropout,
        )
        self.drop1 = layers.Dropout(self.dropout)

        self.norm2 = layers.LayerNormalization(epsilon=1e-6)
        hidden_dim = int(self.embed_dim * self.mlp_ratio)
        self.mlp = tf.keras.Sequential(
            [
                layers.Dense(hidden_dim, activation="gelu"),
                layers.Dropout(self.dropout),
                layers.Dense(self.embed_dim),
                layers.Dropout(self.dropout),
            ]
        )

    def call(self, x, training: bool = False):
        x_attn = self.attn(self.norm1(x), self.norm1(x), training=training)
        x = x + self.drop1(x_attn, training=training)
        x = x + self.mlp(self.norm2(x), training=training)
        return x

    def get_config(self) -> dict[str, object]:
        cfg = super().get_config()
        cfg.update(
            {
                "embed_dim": self.embed_dim,
                "num_heads": self.num_heads,
                "mlp_ratio": self.mlp_ratio,
                "dropout": self.dropout,
            }
        )
        return cfg


def build_xtinyhar_student(
    window_size: int,
    num_features: int,
    num_classes: int,
    patch_size: int = 20,
    embed_dim: int = 128,
    num_heads: int = 4,
    num_layers: int = 2,
    mlp_ratio: float = 2.0,
    dropout: float = 0.1,
) -> tf.keras.Model:
    """Builds an inertial-transformer-like student model.

    This is a pragmatic TensorFlow equivalent for WISDM-first experiments.
    """

    if window_size % patch_size != 0:
        raise ValueError("window_size must be divisible by patch_size")

    inp = tf.keras.Input(shape=(window_size, num_features), name="input")

    # Patchify using strided Conv1D projection: (B, T, C) -> (B, N_patches, D)
    x = layers.Conv1D(
        filters=embed_dim,
        kernel_size=patch_size,
        strides=patch_size,
        padding="valid",
        name="patch_embed",
    )(inp)
    x = layers.Dropout(dropout, name="patch_dropout")(x)

    for i in range(num_layers):
        x = TransformerEncoderBlock(
            embed_dim=embed_dim,
            num_heads=num_heads,
            mlp_ratio=mlp_ratio,
            dropout=dropout,
            name=f"encoder_{i}",
        )(x)

    x = layers.LayerNormalization(epsilon=1e-6, name="head_norm")(x)
    x = layers.GlobalAveragePooling1D(name="token_pool")(x)
    x = layers.Dropout(dropout, name="head_dropout")(x)
    out = layers.Dense(num_classes, activation="softmax", name="classifier")(x)

    return tf.keras.Model(inp, out, name="xtinyhar_student")


def build_xtinyhar_student_conv2d(
    window_size: int,
    num_features: int,
    num_classes: int,
    patch_size: int = 20,
    embed_dim: int = 128,
    num_heads: int = 4,
    num_layers: int = 2,
    mlp_ratio: float = 2.0,
    dropout: float = 0.1,
) -> tf.keras.Model:
    """Conv2D-equivalent XTinyHAR student for QAT-safe execution.

    Conv1D(patch_size, stride=patch_size) on (B, T, C) is mapped to:
    Conv2D((patch_size, 1), stride=(patch_size, 1)) on (B, T, 1, C).
    """

    if window_size % patch_size != 0:
        raise ValueError("window_size must be divisible by patch_size")

    n_patches = window_size // patch_size
    inp = tf.keras.Input(shape=(window_size, num_features), name="input")
    x = layers.Reshape((window_size, 1, num_features), name="reshape_in")(inp)
    x = layers.Conv2D(
        filters=embed_dim,
        kernel_size=(patch_size, 1),
        strides=(patch_size, 1),
        padding="valid",
        name="patch_embed",
    )(x)
    x = layers.Reshape((n_patches, embed_dim), name="patch_tokens")(x)
    x = layers.Dropout(dropout, name="patch_dropout")(x)

    for i in range(num_layers):
        x = TransformerEncoderBlock(
            embed_dim=embed_dim,
            num_heads=num_heads,
            mlp_ratio=mlp_ratio,
            dropout=dropout,
            name=f"encoder_{i}",
        )(x)

    x = layers.LayerNormalization(epsilon=1e-6, name="head_norm")(x)
    x = layers.GlobalAveragePooling1D(name="token_pool")(x)
    x = layers.Dropout(dropout, name="head_dropout")(x)
    out = layers.Dense(num_classes, activation="softmax", name="classifier")(x)
    return tf.keras.Model(inp, out, name="xtinyhar_student_conv2d")


def compile_xtinyhar_student(model: tf.keras.Model, learning_rate: float = 1e-4) -> tf.keras.Model:
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model
