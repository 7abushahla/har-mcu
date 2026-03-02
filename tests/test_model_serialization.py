from __future__ import annotations

import numpy as np
import pytest


tf = pytest.importorskip("tensorflow")

from src.models.serialization import load_checkpoint_model
from src.models.xtinyhar_student_tf import build_xtinyhar_student


def test_xtinyhar_checkpoint_roundtrip_with_safe_loader(tmp_path):
    model = build_xtinyhar_student(
        window_size=200,
        num_features=3,
        num_classes=6,
        patch_size=20,
        embed_dim=64,
        num_heads=2,
        num_layers=2,
    )
    ckpt_path = tmp_path / "xtinyhar_roundtrip.keras"
    model.save(ckpt_path)

    loaded = load_checkpoint_model(ckpt_path, compile=False)
    assert loaded.output_shape[-1] == 6

    x = np.zeros((2, 200, 3), dtype=np.float32)
    y = loaded.predict(x, verbose=0)
    assert y.shape == (2, 6)
