"""Reference TensorFlow Lite Micro op set from micro_mutable_op_resolver.h."""

from __future__ import annotations

from typing import Any

# Provenance (source-of-truth policy for deploy gate):
#   https://github.com/tensorflow/tflite-micro/blob/main/tensorflow/lite/micro/micro_mutable_op_resolver.h
# Snapshot date:
#   2026-03-05
# Snapshot commit hash:
#   f2a058296dd
#
# NOTE:
#   This repo uses this set as deploy-gate source-of-truth for TFLM op support.
#   It is a TFLM-version capability gate, not a universal per-MCU runtime
#   guarantee.
REFERENCE_OPS_MICRO_MUTABLE_MAIN = {
    "ADD",
    "ARG_MAX",
    "ARG_MIN",
    "AVERAGE_POOL_2D",
    "BATCH_MATMUL",
    "BATCH_TO_SPACE_ND",
    "CAST",
    "CEIL",
    "CIRCULAR_BUFFER",
    "CONCATENATION",
    "CONV_2D",
    "COS",
    "CUMSUM",
    "DEPTH_TO_SPACE",
    "DEPTHWISE_CONV_2D",
    "DEQUANTIZE",
    "DIV",
    "ELU",
    "EQUAL",
    "ETHOSU",
    "EXP",
    "EXPAND_DIMS",
    "FILL",
    "FLOOR",
    "FLOOR_DIV",
    "FLOOR_MOD",
    "FULLY_CONNECTED",
    "GATHER",
    "GATHER_ND",
    "GREATER",
    "GREATER_EQUAL",
    "HARD_SWISH",
    "IF",
    "L2_NORMALIZATION",
    "L2_POOL_2D",
    "LEAKY_RELU",
    "LESS",
    "LESS_EQUAL",
    "LOG",
    "LOG_SOFTMAX",
    "LOGICAL_AND",
    "LOGICAL_NOT",
    "LOGICAL_OR",
    "LOGISTIC",
    "MAX_POOL_2D",
    "MAXIMUM",
    "MEAN",
    "MINIMUM",
    "MIRROR_PAD",
    "MUL",
    "NEG",
    "NOT_EQUAL",
    "PACK",
    "PAD",
    "PADV2",
    "PRELU",
    "QUANTIZE",
    "READ_VARIABLE",
    "REDUCE_MAX",
    "REDUCE_MIN",
    "RELU",
    "RELU_0_TO_1",
    "RELU_N1_TO_1",
    "RELU6",
    "RESHAPE",
    "RESIZE_BILINEAR",
    "RESIZE_NEAREST_NEIGHBOR",
    "ROUND",
    "RSQRT",
    "SELECT_V2",
    "SHAPE",
    "SIN",
    "SLICE",
    "SOFTMAX",
    "SPACE_TO_BATCH_ND",
    "SPACE_TO_DEPTH",
    "SPLIT",
    "SPLIT_V",
    "SQRT",
    "SQUARE",
    "SQUARED_DIFFERENCE",
    "SQUEEZE",
    "STRIDED_SLICE",
    "SUB",
    "SVDF",
    "TANH",
    "TRANSPOSE",
    "TRANSPOSE_CONV",
    "UNIDIRECTIONAL_SEQUENCE_LSTM",
    "UNPACK",
    "VAR_HANDLE",
    "WHILE",
    "ZEROS_LIKE",
}

# Backward-compatible alias for older code/tests.
REFERENCE_OPS_ANDROID_A444526 = REFERENCE_OPS_MICRO_MUTABLE_MAIN


def classify_ops_against_reference(ops: list[str] | tuple[str, ...]) -> dict[str, Any]:
    op_set = {str(op).strip() for op in ops if str(op).strip()}
    present = sorted(op for op in op_set if op in REFERENCE_OPS_MICRO_MUTABLE_MAIN)
    absent = sorted(op for op in op_set if op not in REFERENCE_OPS_MICRO_MUTABLE_MAIN)
    return {
        "reference_tag": "micro_mutable_main",
        "supported_in_reference": present,
        "unsupported_in_reference": absent,
    }
