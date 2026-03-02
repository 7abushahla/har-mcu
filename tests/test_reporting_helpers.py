from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.eval.reporting import append_master_results, export_paper_results


def test_export_paper_results_writes_csv_and_md(tmp_path: Path):
    rows = [
        {
            "paper_slug": "xtinyhar",
            "protocol": "random_stratified",
            "variant": "xtinyhar_student",
            "run_mode": "sanity_check",
            "train_device": "gpu",
            "ptq_device": "gpu",
            "qat_device": "cpu",
            "fp32_training_time_sec": 12.4,
            "ptq_inference_latency_ms_median": 0.45,
            "ptq_inference_latency_ms_p95": 0.60,
            "accuracy": 0.95,
            "macro_f1": 0.94,
        }
    ]
    out = export_paper_results(tmp_path, paper_slug="xtinyhar", protocol="random_stratified", rows=rows)
    assert Path(out["csv"]).exists()
    assert Path(out["md"]).exists()

    df = pd.read_csv(out["csv"])
    assert len(df) == 1
    assert df.iloc[0]["paper_slug"] == "xtinyhar"
    assert df.iloc[0]["run_mode"] == "sanity_check"
    assert df.iloc[0]["qat_device"] == "cpu"
    assert float(df.iloc[0]["fp32_training_time_sec"]) == 12.4
    assert float(df.iloc[0]["ptq_inference_latency_ms_median"]) == 0.45


def test_append_master_results_deduplicates_by_run_identity(tmp_path: Path):
    rows_a = [
        {
            "paper_slug": "xtinyhar",
            "protocol": "random_stratified",
            "variant": "xtinyhar_student",
            "run_id": "r0",
            "run_mode": "full_run",
            "compression_focus": "ptq_qat_only",
            "train_device": "cpu",
            "fp32_training_time_sec": 1.2,
            "accuracy": 0.95,
        }
    ]
    rows_b = [
        {
            "paper_slug": "xtinyhar",
            "protocol": "random_stratified",
            "variant": "xtinyhar_student",
            "run_id": "r0",
            "run_mode": "full_run",
            "compression_focus": "ptq_qat_only",
            "train_device": "cpu",
            "fp32_training_time_sec": 1.3,
            "accuracy": 0.96,
        }
    ]

    append_master_results(tmp_path, rows_a)
    out = append_master_results(tmp_path, rows_b)
    df = pd.read_csv(out["csv"])

    assert len(df) == 1
    assert float(df.iloc[0]["accuracy"]) == 0.96
    assert df.iloc[0]["run_mode"] == "full_run"
    assert df.iloc[0]["compression_focus"] == "ptq_qat_only"
    assert float(df.iloc[0]["fp32_training_time_sec"]) == 1.3
