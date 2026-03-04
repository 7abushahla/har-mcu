from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

pytest.importorskip("tensorflow")
from src.eval import notebook_reporting as nr


def _write_json(path: Path, payload: dict) -> str:
    path.write_text(json.dumps(payload), encoding="utf-8")
    return str(path)


def test_build_run_rows_df():
    out = {"rows": [{"protocol": "random_stratified", "accuracy": 0.9}]}
    df = nr.build_run_rows_df(out)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df.iloc[0]["protocol"] == "random_stratified"


def test_build_model_size_summary_df_includes_fp32_ptq_qat_columns():
    rows = [
        {
            "protocol": "random_stratified",
            "fp32_model_size_kb": 120.1,
            "ptq_model_size_kb": 12.0,
            "qat_model_size_kb": 13.0,
            "fp32_tflite_status": "ok",
            "fp32_tflite_model": "/tmp/fp32.tflite",
        }
    ]
    df = nr.build_model_size_summary_df(rows)
    expected_cols = {
        "protocol",
        "fp32_model_size_kb",
        "ptq_model_size_kb",
        "qat_model_size_kb",
        "fp32_tflite_status",
        "fp32_tflite_model",
    }
    assert expected_cols.issubset(df.columns)
    assert float(df.iloc[0]["fp32_model_size_kb"]) == pytest.approx(120.1)
    assert df.iloc[0]["fp32_tflite_status"] == "ok"


def test_build_ptq_operator_visibility_reports_mismatch(tmp_path: Path):
    ptq_eval = _write_json(tmp_path / "ptq_eval.json", {"interpreter_ops": ["CONV_2D", "SOFTMAX"]})
    ptq_report = _write_json(tmp_path / "ptq_report.json", {"tflm_ops": ["CONV_2D", "RESHAPE"]})
    rows = [{"protocol": "random_stratified", "ptq_metrics_json": ptq_eval, "ptq_report_json": ptq_report}]

    visibility, warnings = nr.build_ptq_operator_visibility(rows)
    assert len(visibility) == 1
    assert visibility[0]["only_interpreter"] == ["SOFTMAX"]
    assert visibility[0]["only_tflm"] == ["RESHAPE"]
    assert warnings
    assert "random_stratified" in warnings[0]


def test_build_strict_deploy_table_and_legacy_detection(tmp_path: Path):
    ptq_report = _write_json(
        tmp_path / "ptq_report.json",
        {
            "status": "failed",
            "full_integer_io": True,
            "tflm_compatible": False,
            "unsupported_ops_micro_mutable": ["SUB"],
            "unsupported_ops": ["SUB"],
            "compatibility_scope": "micro_mutable_main",
            "error": "Unsupported ops for micro_mutable_op_resolver.h source: SUB",
        },
    )
    qat_report = _write_json(
        tmp_path / "qat_report.json",
        {
            "status": "ok",
            "qat_status": "ok",
            "full_integer_io": True,
            "tflm_compatible": True,
            "allowed_ops_profile": "nano33ble_extended",
            "allowed_ops_used": ["SUB"],
            "unsupported_ops": [],
        },
    )
    rows = [
        {
            "protocol": "random_stratified",
            "ptq_status": "failed",
            "qat_status": "ok",
            "ptq_report_json": ptq_report,
            "qat_report_json": qat_report,
        }
    ]

    strict_df, legacy, lines = nr.build_strict_deploy_table(rows)
    assert len(strict_df) == 2
    assert legacy is True  # PTQ report intentionally omits allowed_ops_profile/allowed_ops_used
    assert any("ptq_status=failed" in line for line in lines)
    ptq_row = strict_df[strict_df["tier"] == "PTQ"].iloc[0]
    assert ptq_row["status"] == "failed"
    assert ptq_row["compatibility_scope"] == "micro_mutable_main"
    assert ptq_row["unsupported_ops_micro_mutable"] == "SUB"


def test_build_notebook_comparison_df_reuses_canonical_rows():
    cfg = {"experiment": {"paper_targets": {"fp32_accuracy": 0.9, "ptq_accuracy": 0.89, "qat_accuracy": None}}}
    out = {
        "rows": [
            {
                "protocol": "random_stratified",
                "accuracy": 0.91,
                "macro_f1": 0.9,
                "fp32_training_time_sec": 10.0,
                "fp32_model_size_kb": 120.0,
                "ptq_accuracy": 0.9,
                "ptq_macro_f1": 0.89,
                "ptq_model_size_kb": 12.0,
                "ptq_status": "ok",
                "ptq_inference_latency_ms_median": 0.4,
                "ptq_inference_latency_ms_p95": 0.6,
                "qat_accuracy": None,
                "qat_macro_f1": None,
                "qat_model_size_kb": None,
                "qat_status": "failed",
                "qat_training_time_sec": None,
                "qat_inference_latency_ms_median": None,
                "qat_inference_latency_ms_p95": None,
            }
        ]
    }
    df = nr.build_notebook_comparison_df(cfg, out)
    assert {"pipeline", "protocol", "model", "ptq_status", "qat_status", "status"}.issubset(df.columns)
    fp32_row = df[(df["pipeline"] == "WISDM replication") & (df["model"] == "baseline float")].iloc[0]
    assert float(fp32_row["model_size_kb"]) == pytest.approx(120.0)


def test_build_reproducibility_drift_df(tmp_path: Path, monkeypatch):
    split_path = tmp_path / "split_random.npz"
    np.savez(split_path, split_hash=np.array("abc123", dtype=object))

    repeat_metrics = _write_json(tmp_path / "repeat.json", {"accuracy": 0.9})

    monkeypatch.setattr(nr, "split_npz_path", lambda *args, **kwargs: split_path)
    monkeypatch.setattr(nr, "model_ckpt_path", lambda *args, **kwargs: tmp_path / "model.keras")
    monkeypatch.setattr(
        nr,
        "evaluate_model_for_protocol",
        lambda *args, **kwargs: {"metrics_json": repeat_metrics},
    )

    cfg = {
        "paths": {
            "processed_dir": str(tmp_path / "processed"),
            "checkpoints_dir": str(tmp_path / "checkpoints"),
            "reports_dir": str(tmp_path / "reports"),
        },
        "experiment": {"paper_slug": "xtinyhar"},
    }
    out = {
        "rows": [
            {
                "protocol": "random_stratified",
                "window_size": 200,
                "run_id": "wisdm_r0",
                "variant": "xtinyhar_student_conv2d",
                "accuracy": 0.9,
            }
        ]
    }

    drift_df = nr.build_reproducibility_drift_df(cfg, out, drift_tol=1e-9)
    assert len(drift_df) == 1
    assert drift_df.iloc[0]["status"] == "PASS"
