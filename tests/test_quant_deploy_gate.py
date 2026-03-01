from __future__ import annotations

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
    assert "Unsupported TFLM ops: WHILE" in str(out["error"])
