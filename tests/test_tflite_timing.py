from __future__ import annotations

import pytest

pytest.importorskip("tensorflow")

from src.eval.eval_tflite import _summarize_latency_ms


def test_summarize_latency_ms_with_values():
    summary = _summarize_latency_ms([1.0, 2.0, 3.0, 4.0, 5.0])
    assert summary["inference_latency_ms_median"] == pytest.approx(3.0)
    assert summary["inference_latency_ms_p95"] == pytest.approx(4.8, rel=1e-6)
    assert summary["inference_latency_ms_mean"] == pytest.approx(3.0)


def test_summarize_latency_ms_empty_values():
    summary = _summarize_latency_ms([])
    assert summary["inference_latency_ms_median"] is None
    assert summary["inference_latency_ms_p95"] is None
    assert summary["inference_latency_ms_mean"] is None
