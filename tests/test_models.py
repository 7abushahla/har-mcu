from __future__ import annotations

import pytest


tf = pytest.importorskip("tensorflow")

from src.models.daghero_cnn_searchspace_tf import (
    build_daghero_2layer,
    build_daghero_2layer_conv2d,
)
from src.models.deepconv_lstm import build_deepconv_lstm
from src.models.repmobile_folded_tf import build_repmobile_folded, build_repmobile_folded_conv2d
from src.models.tcn_attention_har_tf import (
    build_tcn_attention_har_teacher,
    build_tcn_attention_har_teacher_conv2d,
)
from src.models.tcn_inception_tf import build_tcn_inception, build_tcn_inception_conv2d
from src.models.xtinyhar_student_tf import build_xtinyhar_student, build_xtinyhar_student_conv2d


def test_deepconv_lstm_output_shape():
    model = build_deepconv_lstm(window_size=100, num_features=3, num_classes=6, dropout=0.3)
    assert model.output_shape[-1] == 6


def test_xtinyhar_student_output_shape():
    model = build_xtinyhar_student(
        window_size=200,
        num_features=3,
        num_classes=6,
        patch_size=20,
        embed_dim=64,
        num_heads=2,
        num_layers=2,
    )
    assert model.output_shape[-1] == 6


def test_repmobile_folded_output_shape():
    model = build_repmobile_folded(window_size=200, num_features=3, num_classes=6)
    assert model.output_shape[-1] == 6


def test_repmobile_folded_conv2d_output_shape():
    model = build_repmobile_folded_conv2d(window_size=200, num_features=3, num_classes=6)
    assert model.output_shape[-1] == 6


def test_tcn_attention_teacher_output_shape():
    model = build_tcn_attention_har_teacher(window_size=200, num_features=3, num_classes=6)
    assert model.output_shape[-1] == 6


def test_tcn_attention_teacher_conv2d_output_shape():
    model = build_tcn_attention_har_teacher_conv2d(window_size=200, num_features=3, num_classes=6)
    assert model.output_shape[-1] == 6


def test_daghero_template_output_shape():
    model = build_daghero_2layer(window_size=200, num_features=3, num_classes=6)
    assert model.output_shape[-1] == 6


def test_daghero_template_conv2d_output_shape():
    model = build_daghero_2layer_conv2d(window_size=200, num_features=3, num_classes=6)
    assert model.output_shape[-1] == 6


def test_tcn_inception_output_shape():
    model = build_tcn_inception(window_size=200, num_features=3, num_classes=6, inception_depth=2)
    assert model.output_shape[-1] == 6


def test_xtinyhar_student_conv2d_output_shape():
    model = build_xtinyhar_student_conv2d(
        window_size=200,
        num_features=3,
        num_classes=6,
        patch_size=20,
        embed_dim=64,
        num_heads=2,
        num_layers=2,
    )
    assert model.output_shape[-1] == 6


def test_tcn_inception_conv2d_output_shape():
    model = build_tcn_inception_conv2d(window_size=200, num_features=3, num_classes=6, inception_depth=2)
    assert model.output_shape[-1] == 6
