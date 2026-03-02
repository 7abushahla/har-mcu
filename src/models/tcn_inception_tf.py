"""TCN-Inception model for sensor-based HAR (WISDM-adapted TensorFlow version)."""

from __future__ import annotations

import tensorflow as tf
from tensorflow.keras import layers


def _kernel_triplet(max_kernel_size: int) -> tuple[int, int, int]:
    kernels = []
    for i in range(3):
        k = max(3, int(max_kernel_size / (2**i)))
        if k % 2 == 0:
            k += 1
        kernels.append(k)
    return tuple(kernels)


def _inception_module(
    x: tf.Tensor,
    filters: int,
    max_kernel_size: int,
    bottleneck_size: int,
    use_bottleneck: bool,
    name: str,
) -> tf.Tensor:
    inp = x
    if use_bottleneck and int(x.shape[-1]) > 1:
        x = layers.Conv1D(bottleneck_size, 1, padding="same", activation="relu", name=f"{name}_bneck")(x)

    k1, k2, k3 = _kernel_triplet(max_kernel_size)
    b1 = layers.Conv1D(filters, k1, padding="same", use_bias=False, name=f"{name}_k1")(x)
    b2 = layers.Conv1D(filters, k2, padding="same", use_bias=False, name=f"{name}_k2")(x)
    b3 = layers.Conv1D(filters, k3, padding="same", use_bias=False, name=f"{name}_k3")(x)

    b4 = layers.MaxPool1D(pool_size=3, strides=1, padding="same", name=f"{name}_pool")(inp)
    b4 = layers.Conv1D(filters, 1, padding="same", use_bias=False, name=f"{name}_pool_proj")(b4)

    x = layers.Concatenate(name=f"{name}_concat")([b1, b2, b3, b4])
    x = layers.BatchNormalization(name=f"{name}_bn")(x)
    x = layers.ReLU(name=f"{name}_relu")(x)
    return x


def _tcn_block(
    x: tf.Tensor,
    filters: int,
    kernel_size: int,
    dilation: int,
    name: str,
) -> tf.Tensor:
    inp = x
    x = layers.Conv1D(
        filters,
        kernel_size,
        padding="causal",
        dilation_rate=dilation,
        use_bias=False,
        name=f"{name}_conv1",
    )(x)
    x = layers.BatchNormalization(name=f"{name}_bn1")(x)
    x = layers.ReLU(name=f"{name}_relu1")(x)

    x = layers.Conv1D(
        filters,
        kernel_size,
        padding="causal",
        dilation_rate=dilation,
        use_bias=False,
        name=f"{name}_conv2",
    )(x)
    x = layers.BatchNormalization(name=f"{name}_bn2")(x)
    x = layers.ReLU(name=f"{name}_relu2")(x)

    if int(inp.shape[-1]) != filters:
        inp = layers.Conv1D(filters, 1, padding="same", name=f"{name}_proj")(inp)
    return layers.Add(name=f"{name}_add")([inp, x])


def _causal_conv2d_time(
    x: tf.Tensor,
    filters: int,
    kernel_size: int,
    dilation: int,
    use_bias: bool,
    name: str,
) -> tf.Tensor:
    pad = int(dilation) * (int(kernel_size) - 1)
    if pad > 0:
        x = layers.ZeroPadding2D(padding=((pad, 0), (0, 0)), name=f"{name}_pad")(x)
    return layers.Conv2D(
        filters,
        kernel_size=(kernel_size, 1),
        padding="valid",
        dilation_rate=(dilation, 1),
        use_bias=use_bias,
        name=name,
    )(x)


def _inception_module_conv2d(
    x: tf.Tensor,
    filters: int,
    max_kernel_size: int,
    bottleneck_size: int,
    use_bottleneck: bool,
    name: str,
) -> tf.Tensor:
    inp = x
    if use_bottleneck and int(x.shape[-1]) > 1:
        x = layers.Conv2D(bottleneck_size, (1, 1), padding="same", activation="relu", name=f"{name}_bneck")(x)

    k1, k2, k3 = _kernel_triplet(max_kernel_size)
    b1 = layers.Conv2D(filters, (k1, 1), padding="same", use_bias=False, name=f"{name}_k1")(x)
    b2 = layers.Conv2D(filters, (k2, 1), padding="same", use_bias=False, name=f"{name}_k2")(x)
    b3 = layers.Conv2D(filters, (k3, 1), padding="same", use_bias=False, name=f"{name}_k3")(x)

    b4 = layers.MaxPool2D(pool_size=(3, 1), strides=(1, 1), padding="same", name=f"{name}_pool")(inp)
    b4 = layers.Conv2D(filters, (1, 1), padding="same", use_bias=False, name=f"{name}_pool_proj")(b4)

    x = layers.Concatenate(name=f"{name}_concat")([b1, b2, b3, b4])
    x = layers.BatchNormalization(name=f"{name}_bn")(x)
    x = layers.ReLU(name=f"{name}_relu")(x)
    return x


def _tcn_block_conv2d(
    x: tf.Tensor,
    filters: int,
    kernel_size: int,
    dilation: int,
    name: str,
) -> tf.Tensor:
    inp = x
    x = _causal_conv2d_time(
        x,
        filters=filters,
        kernel_size=kernel_size,
        dilation=dilation,
        use_bias=False,
        name=f"{name}_conv1",
    )
    x = layers.BatchNormalization(name=f"{name}_bn1")(x)
    x = layers.ReLU(name=f"{name}_relu1")(x)

    x = _causal_conv2d_time(
        x,
        filters=filters,
        kernel_size=kernel_size,
        dilation=dilation,
        use_bias=False,
        name=f"{name}_conv2",
    )
    x = layers.BatchNormalization(name=f"{name}_bn2")(x)
    x = layers.ReLU(name=f"{name}_relu2")(x)

    if int(inp.shape[-1]) != filters:
        inp = layers.Conv2D(filters, (1, 1), padding="same", name=f"{name}_proj")(inp)
    return layers.Add(name=f"{name}_add")([inp, x])


def build_tcn_inception(
    window_size: int,
    num_features: int,
    num_classes: int,
    max_kernel_size: int = 68,
    bottleneck_size: int = 32,
    inception_depth: int = 5,
    inception_filters: int = 16,
    tcn_filters: int = 16,
    tcn_kernel_size: int = 3,
    dilations: tuple[int, int, int, int] = (1, 2, 4, 8),
    use_bottleneck: bool = True,
    use_residual: bool = True,
    dropout: float = 0.2,
) -> tf.keras.Model:
    """Build TCN-Inception architecture with paper-style defaults."""

    inp = tf.keras.Input(shape=(window_size, num_features), name="input")
    x = inp

    for i in range(inception_depth):
        x_prev = x
        x = _inception_module(
            x,
            filters=inception_filters,
            max_kernel_size=max_kernel_size,
            bottleneck_size=bottleneck_size,
            use_bottleneck=use_bottleneck,
            name=f"inception_{i}",
        )
        if use_residual and int(x_prev.shape[-1]) == int(x.shape[-1]):
            x = layers.Add(name=f"inception_res_{i}")([x_prev, x])

    for d in dilations:
        x = _tcn_block(
            x,
            filters=tcn_filters,
            kernel_size=tcn_kernel_size,
            dilation=d,
            name=f"tcn_d{d}",
        )

    x = layers.GlobalAveragePooling1D(name="gap")(x)
    x = layers.Dropout(dropout, name="head_drop")(x)
    out = layers.Dense(num_classes, activation="softmax", name="classifier")(x)
    return tf.keras.Model(inp, out, name="tcn_inception")


def build_tcn_inception_conv2d(
    window_size: int,
    num_features: int,
    num_classes: int,
    max_kernel_size: int = 68,
    bottleneck_size: int = 32,
    inception_depth: int = 5,
    inception_filters: int = 16,
    tcn_filters: int = 16,
    tcn_kernel_size: int = 3,
    dilations: tuple[int, int, int, int] = (1, 2, 4, 8),
    use_bottleneck: bool = True,
    use_residual: bool = True,
    dropout: float = 0.2,
) -> tf.keras.Model:
    """Conv2D-equivalent TCN-Inception architecture for QAT-safe runs."""

    inp = tf.keras.Input(shape=(window_size, num_features), name="input")
    x = layers.Reshape((window_size, 1, num_features), name="reshape_in")(inp)

    for i in range(inception_depth):
        x_prev = x
        x = _inception_module_conv2d(
            x,
            filters=inception_filters,
            max_kernel_size=max_kernel_size,
            bottleneck_size=bottleneck_size,
            use_bottleneck=use_bottleneck,
            name=f"inception_{i}",
        )
        if use_residual and int(x_prev.shape[-1]) == int(x.shape[-1]):
            x = layers.Add(name=f"inception_res_{i}")([x_prev, x])

    for d in dilations:
        x = _tcn_block_conv2d(
            x,
            filters=tcn_filters,
            kernel_size=tcn_kernel_size,
            dilation=d,
            name=f"tcn_d{d}",
        )

    x = layers.GlobalAveragePooling2D(name="gap")(x)
    x = layers.Dropout(dropout, name="head_drop")(x)
    out = layers.Dense(num_classes, activation="softmax", name="classifier")(x)
    return tf.keras.Model(inp, out, name="tcn_inception_conv2d")


def compile_tcn_inception(model: tf.keras.Model, learning_rate: float = 5e-4, l2_weight: float = 0.01) -> tf.keras.Model:
    # L2 regularization is provided as optimizer weight decay approximation.
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model
