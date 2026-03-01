from __future__ import annotations

import pytest


tf = pytest.importorskip("tensorflow")

from src.models.deepconv_lstm import build_deepconv_lstm


def test_deepconv_lstm_output_shape():
    model = build_deepconv_lstm(window_size=100, num_features=3, num_classes=6, dropout=0.3)
    assert model.output_shape[-1] == 6
