from __future__ import annotations

import numpy as np
import pytest

pytest.importorskip("tensorflow")

import src.eval.eval_tflite as eval_tflite


def test_build_tflite_interpreter_disables_default_delegates(monkeypatch, tmp_path):
    captured: dict[str, object] = {}

    class DummyInterpreter:
        def __init__(self, *args, **kwargs):
            captured["args"] = args
            captured["kwargs"] = kwargs

    monkeypatch.setattr(eval_tflite.tf.lite, "Interpreter", DummyInterpreter)

    eval_tflite._build_tflite_interpreter(tmp_path / "dummy.tflite")
    kwargs = captured["kwargs"]
    assert kwargs["experimental_op_resolver_type"] == (
        eval_tflite.tf.lite.experimental.OpResolverType.BUILTIN_WITHOUT_DEFAULT_DELEGATES
    )
    assert kwargs["experimental_delegates"] == []
    assert kwargs["num_threads"] == 1


class _FakeInterpreter:
    def __init__(self):
        self._invokes = 0

    def allocate_tensors(self):
        return None

    def get_input_details(self):
        return [{"index": 0, "dtype": np.float32, "quantization": (0.0, 0)}]

    def get_output_details(self):
        return [{"index": 0, "dtype": np.float32, "quantization": (0.0, 0)}]

    def set_tensor(self, index, value):
        return None

    def invoke(self):
        self._invokes += 1

    def get_tensor(self, index):
        return np.asarray([[0.1, 0.9]], dtype=np.float32)

    def _get_ops_details(self):
        return [{"op_name": "CONV_2D"}, {"op_name": "SOFTMAX"}, {"op_name": "SOFTMAX"}]


def test_predict_and_latency_capture_ops_via_shared_interpreter_builder(monkeypatch):
    calls = {"count": 0}

    def _fake_builder(model_path):
        calls["count"] += 1
        return _FakeInterpreter()

    monkeypatch.setattr(eval_tflite, "_build_tflite_interpreter", _fake_builder)

    x = np.zeros((5, 8, 3), dtype=np.float32)
    preds, input_dtype, output_dtype, ops = eval_tflite._run_tflite_predict("dummy.tflite", x)

    assert calls["count"] == 1
    assert preds.shape == (5,)
    assert set(preds.tolist()) == {1}
    assert "float32" in input_dtype
    assert "float32" in output_dtype
    assert ops == ["CONV_2D", "SOFTMAX"]

    latency = eval_tflite._measure_tflite_latency_ms(
        "dummy.tflite",
        x,
        warmup_samples=2,
        timed_samples=2,
    )
    assert calls["count"] == 2
    assert latency["warmup_samples"] == 2
    assert latency["timed_samples"] == 2
    assert latency["inference_latency_ms_median"] is not None
    assert latency["inference_latency_ms_p95"] is not None
