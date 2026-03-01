"""DeepConv+LSTM baseline model."""

from __future__ import annotations

import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv1D, Dense, Dropout, Flatten, LSTM


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


def compile_deepconv_lstm(model: tf.keras.Model, learning_rate: float = 0.001) -> tf.keras.Model:
    optimizer = tf.keras.optimizers.RMSprop(learning_rate=learning_rate)
    model.compile(
        loss="categorical_crossentropy",
        optimizer=optimizer,
        metrics=["accuracy"],
    )
    return model
