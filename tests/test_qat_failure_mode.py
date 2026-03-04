from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest


tf = pytest.importorskip("tensorflow")

import src.quant.qat_train as qat_train


def test_qat_conv1d_preflight_returns_failed_payload_when_non_strict(
    tmp_path: Path, monkeypatch
):
    ckpt_path = tmp_path / "dummy.keras"
    ckpt_path.write_text("stub", encoding="utf-8")

    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(200, 3)),
            tf.keras.layers.Conv1D(16, 3, padding="same", activation="relu", name="conv1d"),
            tf.keras.layers.GlobalAveragePooling1D(),
            tf.keras.layers.Dense(6, activation="softmax"),
        ]
    )

    arrays = {
        "X_train": np.zeros((8, 200, 3), dtype=np.float32),
        "y_train": np.array([0, 1, 2, 3, 4, 5, 0, 1], dtype=np.int32),
        "X_val": np.zeros((4, 200, 3), dtype=np.float32),
        "y_val": np.array([0, 1, 2, 3], dtype=np.int32),
    }

    monkeypatch.setattr(qat_train, "ensure_path_dirs", lambda cfg: None)
    monkeypatch.setattr(qat_train, "dataset_exists", lambda *args, **kwargs: True)
    monkeypatch.setattr(qat_train, "load_split_arrays", lambda *args, **kwargs: arrays)
    monkeypatch.setattr(qat_train, "load_checkpoint_model", lambda *args, **kwargs: model)

    cfg = {
        "paths": {
            "processed_dir": str(tmp_path / "processed"),
            "checkpoints_dir": str(tmp_path / "checkpoints"),
            "models_tflite_dir": str(tmp_path / "models_tflite"),
            "reports_dir": str(tmp_path / "reports"),
        },
        "classes": ["Walking", "Jogging", "Upstairs", "Downstairs", "Sitting", "Standing"],
        "train": {"batch_size": 4},
        "quant": {
            "ptq": {"representative_samples": 8},
            "qat": {
                "enabled": True,
                "annotation_policy": "auto",
                "representative_source": "train",
                "representative_samples": 8,
                "strict_full_int8": True,
                "require_tflm_compatible": True,
                "accepted_integer_io_dtypes": ["int8", "uint8"],
                "enforce_full_int8": True,
            },
        },
    }

    out = qat_train.qat_for_protocol(
        cfg,
        window_size=200,
        protocol="random_stratified",
        model_name="xtinyhar_student",
        checkpoint_path=str(ckpt_path),
        run_id="r0",
        raise_on_strict_failure=False,
    )
    assert out["status"] == "failed"
    assert "qat_device_attempted" in out
    assert "qat_device_used" in out
    assert "fallback_triggered" in out
    assert "fallback_reason" in out
    report = json.loads(Path(out["report_json"]).read_text(encoding="utf-8"))
    assert report["status"] == "failed"
    assert report["qat_status"] == "failed"
    assert "Conv1D/SeparableConv1D" in report["error"]
    assert "*_conv2d" in report["error"]
    assert "qat_device_attempted" in report
    assert "qat_device_used" in report
    assert "fallback_triggered" in report
    assert "fallback_reason" in report


def test_qat_separableconv1d_preflight_returns_failed_payload_when_non_strict(
    tmp_path: Path, monkeypatch
):
    ckpt_path = tmp_path / "dummy.keras"
    ckpt_path.write_text("stub", encoding="utf-8")

    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(200, 3)),
            tf.keras.layers.SeparableConv1D(16, 3, padding="same", activation="relu", name="sepconv1d"),
            tf.keras.layers.GlobalAveragePooling1D(),
            tf.keras.layers.Dense(6, activation="softmax"),
        ]
    )

    arrays = {
        "X_train": np.zeros((8, 200, 3), dtype=np.float32),
        "y_train": np.array([0, 1, 2, 3, 4, 5, 0, 1], dtype=np.int32),
        "X_val": np.zeros((4, 200, 3), dtype=np.float32),
        "y_val": np.array([0, 1, 2, 3], dtype=np.int32),
    }

    monkeypatch.setattr(qat_train, "ensure_path_dirs", lambda cfg: None)
    monkeypatch.setattr(qat_train, "dataset_exists", lambda *args, **kwargs: True)
    monkeypatch.setattr(qat_train, "load_split_arrays", lambda *args, **kwargs: arrays)
    monkeypatch.setattr(qat_train, "load_checkpoint_model", lambda *args, **kwargs: model)

    cfg = {
        "paths": {
            "processed_dir": str(tmp_path / "processed"),
            "checkpoints_dir": str(tmp_path / "checkpoints"),
            "models_tflite_dir": str(tmp_path / "models_tflite"),
            "reports_dir": str(tmp_path / "reports"),
        },
        "classes": ["Walking", "Jogging", "Upstairs", "Downstairs", "Sitting", "Standing"],
        "train": {"batch_size": 4},
        "quant": {
            "ptq": {"representative_samples": 8},
            "qat": {
                "enabled": True,
                "annotation_policy": "auto",
                "representative_source": "train",
                "representative_samples": 8,
                "strict_full_int8": True,
                "require_tflm_compatible": True,
                "accepted_integer_io_dtypes": ["int8", "uint8"],
                "enforce_full_int8": True,
            },
        },
    }

    out = qat_train.qat_for_protocol(
        cfg,
        window_size=200,
        protocol="random_stratified",
        model_name="repmobile_folded",
        checkpoint_path=str(ckpt_path),
        run_id="r0",
        raise_on_strict_failure=False,
    )
    assert out["status"] == "failed"
    assert "qat_device_attempted" in out
    assert "qat_device_used" in out
    assert "fallback_triggered" in out
    assert "fallback_reason" in out
    report = json.loads(Path(out["report_json"]).read_text(encoding="utf-8"))
    assert report["status"] == "failed"
    assert report["qat_status"] == "failed"
    assert "Conv1D/SeparableConv1D" in report["error"]
    assert "SeparableConv1D" in report["error"]
    assert "*_conv2d" in report["error"]
    assert "qat_device_attempted" in report
    assert "qat_device_used" in report
    assert "fallback_triggered" in report
    assert "fallback_reason" in report
