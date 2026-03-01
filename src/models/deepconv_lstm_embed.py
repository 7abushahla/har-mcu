"""Embedding-oriented DeepConv+LSTM variant for TinyOL."""

from __future__ import annotations

import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Conv1D, Dense, Dropout, GlobalAveragePooling1D, Input, LSTM


def build_deepconv_lstm_embed(
    window_size: int,
    num_features: int,
    num_classes: int,
    embedding_dim: int = 128,
    dropout: float = 0.3,
) -> tuple[tf.keras.Model, tf.keras.Model]:
    inputs = Input(shape=(window_size, num_features), name="input")
    x = Conv1D(32, 3, activation="relu", name="conv1")(inputs)
    x = Dropout(dropout, name="dropout1")(x)
    x = Conv1D(64, 3, activation="relu", name="conv2")(x)
    x = Dropout(dropout, name="dropout2")(x)
    x = LSTM(100, return_sequences=True, name="lstm")(x)
    x = GlobalAveragePooling1D(name="gap")(x)
    embed = Dense(embedding_dim, activation="relu", name="embedding")(x)
    head = Dropout(dropout, name="dropout3")(embed)
    outputs = Dense(num_classes, activation="softmax", name="classifier")(head)

    classifier_model = Model(inputs=inputs, outputs=outputs, name="deepconv_lstm_embed_cls")
    embed_model = Model(inputs=inputs, outputs=embed, name="deepconv_lstm_embed")
    return classifier_model, embed_model
