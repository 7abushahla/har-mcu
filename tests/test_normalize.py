from __future__ import annotations

import numpy as np

from src.data.normalize import apply_axis_stats, fit_axis_stats


def test_normalization_shapes():
    X = np.random.randn(20, 10, 3).astype(np.float32)
    mean, std = fit_axis_stats(X)
    Xn = apply_axis_stats(X, mean, std)
    assert mean.shape == (1, 1, 3)
    assert std.shape == (1, 1, 3)
    assert Xn.shape == X.shape
