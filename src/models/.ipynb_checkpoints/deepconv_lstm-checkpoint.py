"""DeepConv+LSTM baseline model."""

from __future__ import annotations

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv1D, Conv2D, Dense, Dropout, Flatten, LSTM, Reshape


def build_deepconv_lstm(
    window_size: int,
    num_features: int,
    num_classes: int,
    dropout: float = 0.3,
) -> tf.keras.Model:
    model = Sequential(name="deepconv_lstm")
    model.add(
        Conv1D(
            filters=32,
            kernel_size=3,
            activation="relu",
            input_shape=(window_size, num_features),
            name="conv1",
        )
    )
    model.add(Dropout(dropout, name="dropout1"))
    model.add(Conv1D(filters=64, kernel_size=3, activation="relu", name="conv2"))
    model.add(Dropout(dropout, name="dropout2"))
    model.add(LSTM(units=100, return_sequences=True, name="lstm"))
    model.add(Flatten(name="flatten"))
    model.add(Dropout(dropout, name="dropout3"))
    model.add(Dense(units=num_classes, activation="softmax", name="classifier"))
    return model


def build_deepconv_lstm_conv2d(
    window_size: int,
    num_features: int,
    num_classes: int,
    dropout: float = 0.3,
) -> tf.keras.Model:
    """Conv2D equivalent of build_deepconv_lstm, compatible with tfmot QAT.

    Conv1D(filters, k) == Conv2D(filters, (k, 1)) when the input is reshaped
    (batch, T, F) → (batch, T, 1, F).  Conv2D is supported by tfmot 0.8.0's
    Default8BitQuantizeRegistry; Conv1D is not (TF 2.14 keras.src.* paths).

    Architecture is numerically identical to build_deepconv_lstm.
    Two valid-padded conv(k=3) layers reduce T by 4 total.
    """
    t_out = window_size - 4  # (T-2) after conv1, (T-4) after conv2
    inp = tf.keras.Input(shape=(window_size, num_features), name="input")
    x = Reshape((window_size, 1, num_features), name="reshape_in")(inp)
    x = Conv2D(32, (3, 1), activation="relu", name="conv1")(x)
    x = Dropout(dropout, name="dropout1")(x)
    x = Conv2D(64, (3, 1), activation="relu", name="conv2")(x)
    x = Dropout(dropout, name="dropout2")(x)
    x = Reshape((t_out, 64), name="reshape_squeeze")(x)
    x = LSTM(units=100, return_sequences=True, name="lstm")(x)
    x = Flatten(name="flatten")(x)
    x = Dropout(dropout, name="dropout3")(x)
    out = Dense(units=num_classes, activation="softmax", name="classifier")(x)
    return tf.keras.Model(inputs=inp, outputs=out, name="deepconv_lstm_conv2d")


def compile_deepconv_lstm(model: tf.keras.Model, learning_rate: float = 0.001) -> tf.keras.Model:
    optimizer = tf.keras.optimizers.RMSprop(learning_rate=learning_rate)
    model.compile(
        loss="categorical_crossentropy",
        optimizer=optimizer,
        metrics=["accuracy"],
    )
    return model
