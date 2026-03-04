from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest


pytest.importorskip("tensorflow")

import src.quant.ptq_full_int8 as ptq_full_int8


def test_ptq_failure_payload_includes_ptq_status_alias(tmp_path: Path, monkeypatch):
    ckpt_path = tmp_path / "dummy.keras"
    ckpt_path.write_text("stub", encoding="utf-8")

    monkeypatch.setattr(ptq_full_int8, "ensure_path_dirs", lambda cfg: None)
    monkeypatch.setattr(ptq_full_int8, "dataset_exists", lambda *args, **kwargs: True)
    monkeypatch.setattr(
        ptq_full_int8,
        "load_split_arrays",
        lambda *args, **kwargs: {"X_train": np.zeros((4, 200, 3), dtype=np.float32)},
    )
    monkeypatch.setattr(ptq_full_int8, "load_checkpoint_model", lambda *args, **kwargs: object())

    cfg = {
        "paths": {
            "processed_dir": str(tmp_path / "processed"),
            "checkpoints_dir": str(tmp_path / "checkpoints"),
            "models_tflite_dir": str(tmp_path / "models_tflite"),
            "reports_dir": str(tmp_path / "reports"),
        },
        "quant": {
            "ptq": {
                "representative_source": "invalid_source_for_test",
                "representative_samples": 8,
                "strict_full_int8": True,
                "require_tflm_compatible": True,
                "accepted_integer_io_dtypes": ["int8", "uint8"],
            }
        },
        "deploy": {
            "allowed_ops_profile": "nano33ble_extended",
            "allowed_ops": None,
        },
    }

    with pytest.raises(RuntimeError, match="Invalid representative source"):
        ptq_full_int8.quantize_ptq_for_protocol(
            cfg,
            window_size=200,
            protocol="random_stratified",
            model_name="xtinyhar_student_conv2d",
            checkpoint_path=str(ckpt_path),
            run_id="wisdm_r0",
        )

    report_files = sorted((tmp_path / "reports").glob("ptq_export_*.json"))
    assert report_files, "Expected PTQ report JSON to be written on failure"
    payload = json.loads(report_files[-1].read_text(encoding="utf-8"))
    assert payload["status"] == "failed"
    assert payload["ptq_status"] == "failed"
    assert payload["allowed_ops_profile"] == "nano33ble_extended"
