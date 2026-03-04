from __future__ import annotations

from src.quant import deploy_gate
from src.quant.deploy_gate import evaluate_deploy_gate_from_details


def test_deploy_gate_accepts_int8_and_uint8_io():
    out = evaluate_deploy_gate_from_details(
        input_dtype_raw="<class 'numpy.uint8'>",
        output_dtype_raw="<class 'numpy.int8'>",
        accepted_integer_io_dtypes=["int8", "uint8"],
        strict_full_int8=True,
        require_tflm_compatible=True,
        tflm_compatible=True,
        tflm_ops=["CONV_2D", "UNIDIRECTIONAL_SEQUENCE_LSTM"],
        unsupported_ops=[],
        compat_error=None,
    )
    assert out["status"] == "ok"
    assert out["deployable_full_int8"] is True
    assert out["full_integer_io"] is True
    assert out["compatibility_scope"] == "micro_mutable_main"
    assert out["unsupported_ops_micro_mutable"] == []
    assert out["unsupported_ops_profile"] == []
    assert out["possibly_supported_upstream_tflm"] == []
    assert out["unsupported_in_reference"] == []


def test_deploy_gate_rejects_float_io_under_strict_policy():
    out = evaluate_deploy_gate_from_details(
        input_dtype_raw="<class 'numpy.float32'>",
        output_dtype_raw="<class 'numpy.float32'>",
        accepted_integer_io_dtypes=["int8", "uint8"],
        strict_full_int8=True,
        require_tflm_compatible=True,
        tflm_compatible=True,
        tflm_ops=["CONV_2D"],
        unsupported_ops=[],
        compat_error=None,
    )
    assert out["status"] == "failed"
    assert out["deployable_full_int8"] is False
    assert out["full_integer_io"] is False
    assert "accepted integer dtypes" in str(out["error"])


def test_deploy_gate_rejects_unsupported_ops():
    out = evaluate_deploy_gate_from_details(
        input_dtype_raw="<class 'numpy.int8'>",
        output_dtype_raw="<class 'numpy.int8'>",
        accepted_integer_io_dtypes=["int8", "uint8"],
        strict_full_int8=True,
        require_tflm_compatible=True,
        tflm_compatible=False,
        tflm_ops=["CONV_2D", "WHILE"],
        unsupported_ops=["WHILE"],
        compat_error=None,
    )
    assert out["status"] == "failed"
    assert out["deployable_full_int8"] is False
    assert out["has_while_op"] is True
    assert "micro_mutable_op_resolver.h source" in str(out["error"])
    assert "WHILE" in str(out["error"])
    assert out["unsupported_ops_micro_mutable"] == ["WHILE"]
    assert out["unsupported_ops_profile"] == ["WHILE"]


def test_check_tflm_compat_uses_micro_mutable_source_of_truth(monkeypatch):
    monkeypatch.setattr(
        deploy_gate,
        "_tflite_flatbuffer_ops",
        lambda _path: ["CONV_2D", "MAX_POOL_2D", "MEAN", "DEPTHWISE_CONV_2D"],
    )
    ok, ops, unsupported, compat_error, allowed_used, profile_used = deploy_gate.check_tflm_compat(
        "dummy.tflite",
        allowed_ops_profile="nano33ble_extended",
    )
    assert ok is True
    assert compat_error is None
    assert unsupported == []
    assert "MAX_POOL_2D" in ops
    assert "MEAN" in ops
    assert "DEPTHWISE_CONV_2D" in ops
    assert "MAX_POOL_2D" in allowed_used
    assert profile_used == "micro_mutable_main"


def test_check_tflm_compat_rejects_op_absent_from_micro_mutable_reference(monkeypatch):
    monkeypatch.setattr(
        deploy_gate,
        "_tflite_flatbuffer_ops",
        lambda _path: ["CONV_2D", "REDUCE_PROD"],
    )
    ok, _ops, unsupported, compat_error, allowed_used, profile_used = deploy_gate.check_tflm_compat(
        "dummy.tflite",
        allowed_ops_profile="minimal",
    )
    assert ok is False
    assert compat_error is None
    assert unsupported == ["REDUCE_PROD"]
    assert "REDUCE_PROD" not in allowed_used
    assert profile_used == "micro_mutable_main"
