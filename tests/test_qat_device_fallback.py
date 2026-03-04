from __future__ import annotations

import json
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

tf = pytest.importorskip("tensorflow")

import src.quant.qat_train as qat_train


class _FakeQATModel:
    def compile(self, *args, **kwargs):
        return None

    def fit(self, *args, **kwargs):
        return SimpleNamespace(history={"loss": [1.0], "accuracy": [0.5]})

    def save(self, path):
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("stub", encoding="utf-8")


class _FakeConverter:
    def __init__(self):
        self.optimizations = []
        self.representative_dataset = None
        self.target_spec = SimpleNamespace(supported_ops=[])
        self.inference_input_type = None
        self.inference_output_type = None

    def convert(self):
        return b"fake_tflite"


def _base_cfg(tmp_path: Path, *, device_preference: str, auto_fallback_to_cpu: bool) -> dict:
    return {
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
                "device_preference": device_preference,
                "auto_fallback_to_cpu": auto_fallback_to_cpu,
                "representative_source": "train",
                "representative_samples": 8,
                "strict_full_int8": True,
                "require_tflm_compatible": True,
                "accepted_integer_io_dtypes": ["int8", "uint8"],
                "enforce_full_int8": True,
                "epochs": 1,
                "batch_size": 4,
            },
        },
    }


def _common_monkeypatches(
    monkeypatch: pytest.MonkeyPatch,
    *,
    arrays: dict,
    fp32_model: tf.keras.Model,
    gate_status: str = "ok",
):
    monkeypatch.setattr(qat_train, "ensure_path_dirs", lambda cfg: None)
    monkeypatch.setattr(qat_train, "dataset_exists", lambda *args, **kwargs: True)
    monkeypatch.setattr(qat_train, "load_split_arrays", lambda *args, **kwargs: arrays)
    monkeypatch.setattr(qat_train, "load_checkpoint_model", lambda *args, **kwargs: fp32_model)
    monkeypatch.setattr(qat_train.tf, "device", lambda name: nullcontext())
    monkeypatch.setattr(
        qat_train.tf.lite.TFLiteConverter,
        "from_keras_model",
        lambda model: _FakeConverter(),
    )

    gate_error = None if gate_status == "ok" else "mock gate failure"
    monkeypatch.setattr(
        qat_train,
        "inspect_tflite_and_evaluate_deploy_gate",
        lambda *args, **kwargs: {
            "input_dtype": "<class 'numpy.int8'>",
            "output_dtype": "<class 'numpy.int8'>",
            "input_dtype_normalized": "int8",
            "output_dtype_normalized": "int8",
            "accepted_integer_io_dtypes": ["int8", "uint8"],
            "full_integer_io": True,
            "tflm_compatible": gate_status == "ok",
            "unsupported_ops": [] if gate_status == "ok" else ["MEAN"],
            "tflm_ops": ["CONV_2D"],
            "compat_error": None,
            "has_unidirectional_sequence_lstm": False,
            "has_while_op": False,
            "deployable_full_int8": gate_status == "ok",
            "status": gate_status,
            "error": gate_error,
        },
    )


def test_qat_gpu_determinism_error_falls_back_to_cpu(tmp_path: Path, monkeypatch):
    ckpt_path = tmp_path / "dummy.keras"
    ckpt_path.write_text("stub", encoding="utf-8")

    arrays = {
        "X_train": np.zeros((8, 200, 3), dtype=np.float32),
        "y_train": np.array([0, 1, 2, 3, 4, 5, 0, 1], dtype=np.int32),
        "X_val": np.zeros((4, 200, 3), dtype=np.float32),
        "y_val": np.array([0, 1, 2, 3], dtype=np.int32),
    }
    fp32_model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(200, 3)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(6, activation="softmax"),
        ]
    )

    _common_monkeypatches(monkeypatch, arrays=arrays, fp32_model=fp32_model, gate_status="ok")
    monkeypatch.setattr(
        qat_train.tf.config,
        "list_physical_devices",
        lambda kind: [object()] if str(kind).upper() == "GPU" else [],
    )

    attempts = {"n": 0}

    def _fake_build(*args, **kwargs):
        attempts["n"] += 1
        if attempts["n"] == 1:
            raise RuntimeError("FakeQuantWithMinMaxVarsGradient Determinism failure on GPU")
        return _FakeQATModel(), "mock_policy"

    monkeypatch.setattr(qat_train, "_build_qat_model", _fake_build)

    cfg = _base_cfg(tmp_path, device_preference="gpu", auto_fallback_to_cpu=True)
    out = qat_train.qat_for_protocol(
        cfg,
        window_size=200,
        protocol="random_stratified",
        model_name="xtinyhar_student_conv2d",
        checkpoint_path=str(ckpt_path),
        run_id="r0",
        raise_on_strict_failure=False,
    )
    assert out["status"] == "ok"
    assert out["qat_device_used"] == "/CPU:0"
    assert out["fallback_triggered"] is True
    report = json.loads(Path(out["report_json"]).read_text(encoding="utf-8"))
    assert report["qat_device_attempted"] == ["/GPU:0", "/CPU:0"]
    assert report["qat_device_used"] == "/CPU:0"
    assert report["fallback_triggered"] is True


def test_qat_gpu_preference_without_gpu_uses_cpu_when_fallback_enabled(tmp_path: Path, monkeypatch):
    ckpt_path = tmp_path / "dummy.keras"
    ckpt_path.write_text("stub", encoding="utf-8")

    arrays = {
        "X_train": np.zeros((8, 200, 3), dtype=np.float32),
        "y_train": np.array([0, 1, 2, 3, 4, 5, 0, 1], dtype=np.int32),
        "X_val": np.zeros((4, 200, 3), dtype=np.float32),
        "y_val": np.array([0, 1, 2, 3], dtype=np.int32),
    }
    fp32_model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(200, 3)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(6, activation="softmax"),
        ]
    )

    _common_monkeypatches(monkeypatch, arrays=arrays, fp32_model=fp32_model, gate_status="ok")
    monkeypatch.setattr(
        qat_train.tf.config,
        "list_physical_devices",
        lambda kind: [],
    )
    monkeypatch.setattr(
        qat_train,
        "_build_qat_model",
        lambda *args, **kwargs: (_FakeQATModel(), "mock_policy"),
    )

    cfg = _base_cfg(tmp_path, device_preference="gpu", auto_fallback_to_cpu=True)
    out = qat_train.qat_for_protocol(
        cfg,
        window_size=200,
        protocol="random_stratified",
        model_name="xtinyhar_student_conv2d",
        checkpoint_path=str(ckpt_path),
        run_id="r0",
        raise_on_strict_failure=False,
    )
    assert out["status"] == "ok"
    report = json.loads(Path(out["report_json"]).read_text(encoding="utf-8"))
    assert report["qat_device_attempted"] == ["/CPU:0"]
    assert report["qat_device_used"] == "/CPU:0"
    assert report["fallback_triggered"] is False


def test_qat_gpu_failure_without_fallback_returns_failed_payload(tmp_path: Path, monkeypatch):
    ckpt_path = tmp_path / "dummy.keras"
    ckpt_path.write_text("stub", encoding="utf-8")

    arrays = {
        "X_train": np.zeros((8, 200, 3), dtype=np.float32),
        "y_train": np.array([0, 1, 2, 3, 4, 5, 0, 1], dtype=np.int32),
        "X_val": np.zeros((4, 200, 3), dtype=np.float32),
        "y_val": np.array([0, 1, 2, 3], dtype=np.int32),
    }
    fp32_model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(200, 3)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(6, activation="softmax"),
        ]
    )

    _common_monkeypatches(monkeypatch, arrays=arrays, fp32_model=fp32_model, gate_status="ok")
    monkeypatch.setattr(
        qat_train.tf.config,
        "list_physical_devices",
        lambda kind: [object()] if str(kind).upper() == "GPU" else [],
    )
    monkeypatch.setattr(
        qat_train,
        "_build_qat_model",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("generic GPU QAT failure")),
    )

    cfg = _base_cfg(tmp_path, device_preference="gpu", auto_fallback_to_cpu=False)
    out = qat_train.qat_for_protocol(
        cfg,
        window_size=200,
        protocol="random_stratified",
        model_name="xtinyhar_student_conv2d",
        checkpoint_path=str(ckpt_path),
        run_id="r0",
        raise_on_strict_failure=False,
    )
    assert out["status"] == "failed"
    report = json.loads(Path(out["report_json"]).read_text(encoding="utf-8"))
    assert report["status"] == "failed"
    assert report["qat_device_attempted"] == ["/GPU:0"]
    assert report["qat_device_used"] is None
    assert report["fallback_triggered"] is False
    assert "Unable to construct QAT model" in report["error"]

