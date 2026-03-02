"""TCN-attention-HAR teacher/student TensorFlow implementations."""

from __future__ import annotations

import tensorflow as tf
from tensorflow.keras import layers


def _tcn_residual_block(
    x: tf.Tensor,
    filters: int,
    kernel_size: int,
    dilation_rate: int,
    dropout: float,
    name: str,
) -> tf.Tensor:
    inp = x
    x = layers.Conv1D(
        filters,
        kernel_size,
        padding="causal",
        dilation_rate=dilation_rate,
        use_bias=False,
        name=f"{name}_conv1",
    )(x)
    x = layers.LayerNormalization(name=f"{name}_ln1")(x)
    x = layers.ReLU(name=f"{name}_relu1")(x)
    x = layers.Dropout(dropout, name=f"{name}_drop1")(x)

    x = layers.Conv1D(
        filters,
        kernel_size,
        padding="causal",
        dilation_rate=dilation_rate,
        use_bias=False,
        name=f"{name}_conv2",
    )(x)
    x = layers.LayerNormalization(name=f"{name}_ln2")(x)
    x = layers.ReLU(name=f"{name}_relu2")(x)
    x = layers.Dropout(dropout, name=f"{name}_drop2")(x)

    if int(inp.shape[-1]) != filters:
        inp = layers.Conv1D(filters, 1, padding="same", name=f"{name}_proj")(inp)
    return layers.Add(name=f"{name}_add")([inp, x])


def _causal_conv2d_time(
    x: tf.Tensor,
    filters: int,
    kernel_size: int,
    dilation_rate: int,
    use_bias: bool,
    name: str,
) -> tf.Tensor:
    pad = int(dilation_rate) * (int(kernel_size) - 1)
    if pad > 0:
        x = layers.ZeroPadding2D(padding=((pad, 0), (0, 0)), name=f"{name}_pad")(x)
    return layers.Conv2D(
        filters,
        kernel_size=(kernel_size, 1),
        padding="valid",
        dilation_rate=(dilation_rate, 1),
        use_bias=use_bias,
        name=name,
    )(x)


def _tcn_residual_block_conv2d(
    x: tf.Tensor,
    filters: int,
    kernel_size: int,
    dilation_rate: int,
    dropout: float,
    name: str,
) -> tf.Tensor:
    inp = x
    x = _causal_conv2d_time(
        x,
        filters=filters,
        kernel_size=kernel_size,
        dilation_rate=dilation_rate,
        use_bias=False,
        name=f"{name}_conv1",
    )
    x = layers.LayerNormalization(name=f"{name}_ln1")(x)
    x = layers.ReLU(name=f"{name}_relu1")(x)
    x = layers.Dropout(dropout, name=f"{name}_drop1")(x)

    x = _causal_conv2d_time(
        x,
        filters=filters,
        kernel_size=kernel_size,
        dilation_rate=dilation_rate,
        use_bias=False,
        name=f"{name}_conv2",
    )
    x = layers.LayerNormalization(name=f"{name}_ln2")(x)
    x = layers.ReLU(name=f"{name}_relu2")(x)
    x = layers.Dropout(dropout, name=f"{name}_drop2")(x)

    if int(inp.shape[-1]) != filters:
        inp = layers.Conv2D(filters, (1, 1), padding="same", name=f"{name}_proj")(inp)
    return layers.Add(name=f"{name}_add")([inp, x])


def build_tcn_attention_har_teacher(
    window_size: int,
    num_features: int,
    num_classes: int,
    filters: int = 64,
    kernel_sizes: tuple[int, int, int] = (3, 5, 7),
    dilations: tuple[int, int, int] = (1, 2, 4),
    attention_heads: int = 4,
    dropout: float = 0.2,
) -> tf.keras.Model:
    """Multi-scale TCN + MHA teacher approximation."""

    inp = tf.keras.Input(shape=(window_size, num_features), name="input")

    branches = []
    for k in kernel_sizes:
        x = inp
        for d in dilations:
            x = _tcn_residual_block(
                x,
                filters=filters,
                kernel_size=k,
                dilation_rate=d,
                dropout=dropout,
                name=f"tcn_k{k}_d{d}",
            )
        branches.append(x)

    x = layers.Concatenate(name="concat_multiscale")(branches)
    x = layers.LayerNormalization(name="pre_attn_ln")(x)
    x = layers.MultiHeadAttention(
        num_heads=attention_heads,
        key_dim=max(1, (filters * len(kernel_sizes)) // max(1, attention_heads)),
        dropout=dropout,
        name="mha",
    )(x, x)

    x = layers.GlobalAveragePooling1D(name="gap")(x)
    x = layers.Dropout(dropout, name="head_drop")(x)
    out = layers.Dense(num_classes, activation="softmax", name="classifier")(x)
    return tf.keras.Model(inp, out, name="tcn_attention_har_teacher")


def build_tcn_attention_har_teacher_conv2d(
    window_size: int,
    num_features: int,
    num_classes: int,
    filters: int = 64,
    kernel_sizes: tuple[int, int, int] = (3, 5, 7),
    dilations: tuple[int, int, int] = (1, 2, 4),
    attention_heads: int = 4,
    dropout: float = 0.2,
) -> tf.keras.Model:
    """Conv2D-equivalent multi-scale TCN + MHA teacher."""

    inp = tf.keras.Input(shape=(window_size, num_features), name="input")
    x0 = layers.Reshape((window_size, 1, num_features), name="reshape_in")(inp)

    branches = []
    for k in kernel_sizes:
        x = x0
        for d in dilations:
            x = _tcn_residual_block_conv2d(
                x,
                filters=filters,
                kernel_size=k,
                dilation_rate=d,
                dropout=dropout,
                name=f"tcn_k{k}_d{d}",
            )
        branches.append(x)

    x = layers.Concatenate(axis=-1, name="concat_multiscale")(branches)
    x = layers.Reshape((window_size, filters * len(kernel_sizes)), name="reshape_for_attn")(x)
    x = layers.LayerNormalization(name="pre_attn_ln")(x)
    x = layers.MultiHeadAttention(
        num_heads=attention_heads,
        key_dim=max(1, (filters * len(kernel_sizes)) // max(1, attention_heads)),
        dropout=dropout,
        name="mha",
    )(x, x)
    x = layers.GlobalAveragePooling1D(name="gap")(x)
    x = layers.Dropout(dropout, name="head_drop")(x)
    out = layers.Dense(num_classes, activation="softmax", name="classifier")(x)
    return tf.keras.Model(inp, out, name="tcn_attention_har_teacher_conv2d")


def build_tahar_student_cnn(
    window_size: int,
    num_features: int,
    num_classes: int,
    filters: int = 16,
    dropout: float = 0.2,
) -> tf.keras.Model:
    inp = tf.keras.Input(shape=(window_size, num_features), name="input")
    x = layers.Conv1D(filters, 5, padding="same", activation="relu", name="conv1")(inp)
    x = layers.Conv1D(filters * 2, 3, padding="same", activation="relu", name="conv2")(x)
    x = layers.GlobalAveragePooling1D(name="gap")(x)
    x = layers.Dropout(dropout, name="drop")(x)
    out = layers.Dense(num_classes, activation="softmax", name="classifier")(x)
    return tf.keras.Model(inp, out, name="tahar_student_cnn")


def build_tahar_student_lstm(
    window_size: int,
    num_features: int,
    num_classes: int,
    units: int = 32,
    dropout: float = 0.2,
) -> tf.keras.Model:
    inp = tf.keras.Input(shape=(window_size, num_features), name="input")
    x = layers.LSTM(units, return_sequences=False, name="lstm")(inp)
    x = layers.Dropout(dropout, name="drop")(x)
    out = layers.Dense(num_classes, activation="softmax", name="classifier")(x)
    return tf.keras.Model(inp, out, name="tahar_student_lstm")


def build_tahar_student_gru(
    window_size: int,
    num_features: int,
    num_classes: int,
    units: int = 32,
    dropout: float = 0.2,
) -> tf.keras.Model:
    inp = tf.keras.Input(shape=(window_size, num_features), name="input")
    x = layers.GRU(units, return_sequences=False, name="gru")(inp)
    x = layers.Dropout(dropout, name="drop")(x)
    out = layers.Dense(num_classes, activation="softmax", name="classifier")(x)
    return tf.keras.Model(inp, out, name="tahar_student_gru")


def compile_tcn_attention(model: tf.keras.Model, learning_rate: float = 5e-4) -> tf.keras.Model:
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model
