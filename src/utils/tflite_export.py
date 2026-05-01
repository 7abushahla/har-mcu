"""Shared TFLite conversion helpers.

These mirror the notebook export path for LSTM/TensorList models: make the
batch dimension explicit for conversion and ask TensorFlow Lite to use the
single-batch TensorList lowering when that private converter flag exists.
"""

from __future__ import annotations

from typing import Any


def force_single_batch_input(model: Any, batch_size: int = 1) -> bool:
    """Set dynamic Keras model input batch dimensions to a fixed batch size.

    TensorFlow Lite's LSTM/TensorList converter path is much more reliable when
    the input batch is known at conversion time. This is intentionally best
    effort because different Keras/TensorFlow versions expose input tensors
    slightly differently.
    """

    changed = False
    inputs = getattr(model, "inputs", None) or [getattr(model, "input", None)]
    for tensor in inputs:
        if tensor is None or not hasattr(tensor, "shape") or not hasattr(tensor, "set_shape"):
            continue
        try:
            shape = tensor.shape.as_list()
        except Exception:
            shape = list(tensor.shape)
        if not shape or shape[0] is not None:
            continue
        try:
            tensor.set_shape([int(batch_size), *shape[1:]])
            changed = True
        except Exception:
            continue
    return changed


def enable_single_batch_tensor_list_ops(converter: Any) -> bool:
    """Enable TensorFlow Lite's single-batch TensorList lowering when present."""

    attr = "_experimental_default_to_single_batch_in_tensor_list_ops"
    if hasattr(converter, attr):
        setattr(converter, attr, True)
        return True
    return False
