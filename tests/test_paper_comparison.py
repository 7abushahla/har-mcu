from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from src.eval.paper_comparison import build_paper_comparison_rows, export_paper_comparison


def _sample_rows() -> list[dict]:
    return [
        {
            "protocol": "random_stratified",
            "accuracy": 0.91,
            "macro_f1": 0.90,
            "fp32_training_time_sec": 12.5,
            "ptq_accuracy": 0.90,
            "ptq_macro_f1": 0.89,
            "ptq_model_size_kb": 45.2,
            "ptq_status": "ok",
            "ptq_inference_latency_ms_median": 0.45,
            "ptq_inference_latency_ms_p95": 0.61,
            "qat_accuracy": 0.905,
            "qat_macro_f1": 0.895,
            "qat_model_size_kb": 47.8,
            "qat_status": "ok",
            "qat_training_time_sec": 5.5,
            "qat_inference_latency_ms_median": 0.50,
            "qat_inference_latency_ms_p95": 0.67,
        },
        {
            "protocol": "user_holdout",
            "accuracy": 0.87,
            "macro_f1": 0.86,
            "fp32_training_time_sec": 13.0,
            "ptq_accuracy": 0.86,
            "ptq_macro_f1": 0.85,
            "ptq_model_size_kb": 45.1,
            "ptq_status": "ok",
            "ptq_inference_latency_ms_median": 0.47,
            "ptq_inference_latency_ms_p95": 0.64,
            "qat_accuracy": None,
            "qat_macro_f1": None,
            "qat_model_size_kb": None,
            "qat_status": "failed",
            "qat_training_time_sec": None,
            "qat_inference_latency_ms_median": None,
            "qat_inference_latency_ms_p95": None,
        },
    ]


def test_build_paper_comparison_rows_handles_partial_targets():
    rows = build_paper_comparison_rows(
        _sample_rows(),
        paper_targets={
            "fp32_accuracy": 0.90,
            "ptq_accuracy": 0.89,
            "qat_accuracy": None,
            "notes": "QAT not reported in source paper.",
        },
    )
    assert len(rows) == (2 * 3 + 3)  # three tiers per protocol + three target rows
    fp32_row = next(
        r
        for r in rows
        if r["pipeline"] == "WISDM replication"
        and r["protocol"] == "random_stratified"
        and r["model"] == "baseline float"
    )
    assert fp32_row["acc_delta_vs_target"] == pytest.approx(0.01)
    qat_target = next(r for r in rows if r["pipeline"] == "paper target" and r["model"] == "QAT int8")
    assert qat_target["accuracy"] is None


def test_export_paper_comparison_writes_csv_md_and_plots(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(
        pd.DataFrame,
        "to_markdown",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("should not be called")),
    )

    out = export_paper_comparison(
        tmp_path,
        paper_slug="xtinyhar",
        run_rows=_sample_rows(),
        paper_targets={
            "fp32_accuracy": 0.90,
            "ptq_accuracy": 0.89,
            "qat_accuracy": None,
            "notes": "QAT not reported in source paper.",
        },
    )
    for key in ("csv", "md", "accuracy_png", "size_png", "latency_png"):
        assert key in out
        assert Path(out[key]).exists()

    df = pd.read_csv(out["csv"])
    expected_cols = {
        "pipeline",
        "protocol",
        "model",
        "accuracy",
        "macro_f1",
        "model_size_kb",
        "training_time_sec",
        "inference_latency_ms_median",
        "inference_latency_ms_p95",
        "paper_target_accuracy",
        "acc_delta_vs_target",
        "status",
    }
    assert expected_cols.issubset(set(df.columns))
