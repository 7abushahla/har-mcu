from __future__ import annotations

from src.deploy.tflm_reference_ops import (
    REFERENCE_OPS_MICRO_MUTABLE_MAIN,
    classify_ops_against_reference,
)


def test_reference_set_contains_expected_ops():
    expected = {
        "CONCATENATION",
        "PAD",
        "RSQRT",
        "SUB",
        "SPACE_TO_BATCH_ND",
        "BATCH_TO_SPACE_ND",
        "BATCH_MATMUL",
        "FILL",
        "SQUARED_DIFFERENCE",
    }
    assert expected.issubset(REFERENCE_OPS_MICRO_MUTABLE_MAIN)


def test_classify_ops_against_reference_splits_supported_and_unsupported():
    out = classify_ops_against_reference(["CONCATENATION", "REDUCE_PROD", "SUB"])
    assert out["reference_tag"] == "micro_mutable_main"
    assert out["supported_in_reference"] == ["CONCATENATION", "SUB"]
    assert out["unsupported_in_reference"] == ["REDUCE_PROD"]
