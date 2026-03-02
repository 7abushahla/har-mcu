"""Helpers for robust Keras checkpoint loading across paper models."""

from __future__ import annotations

from importlib import import_module
from pathlib import Path

import tensorflow as tf


def _ensure_model_modules_imported() -> None:
    # Import model modules so any custom Keras layers are registered.
    for module_name in (
        "src.models.xtinyhar_student_tf",
        "src.models.deepconv_lstm",
        "src.models.repmobile_folded_tf",
        "src.models.tcn_attention_har_tf",
        "src.models.tcn_inception_tf",
        "src.models.daghero_cnn_searchspace_tf",
    ):
        import_module(module_name)


def load_checkpoint_model(path: str | Path, *, compile: bool = False) -> tf.keras.Model:
    """Load a saved `.keras` checkpoint with custom-layer registration in place."""

    _ensure_model_modules_imported()
    from src.models.xtinyhar_student_tf import TransformerEncoderBlock

    custom_objects = {
        "TransformerEncoderBlock": TransformerEncoderBlock,
        "har_mcu>TransformerEncoderBlock": TransformerEncoderBlock,
    }
    return tf.keras.models.load_model(
        Path(path),
        compile=compile,
        custom_objects=custom_objects,
    )
