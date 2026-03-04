from __future__ import annotations

import json
from contextlib import nullcontext
from pathlib import Path

import pytest


pytest.importorskip("tensorflow")

import src.run_paper_experiment as runner
from src.run_paper_experiment import run_paper_experiment


def test_run_paper_experiment_rejects_non_ptq_qat_compression_focus():
    cfg = {
        "experiment": {
            "compression_focus": "kd_only",
        }
    }
    with pytest.raises(ValueError, match="PTQ/QAT"):
        run_paper_experiment(cfg)


def test_run_paper_experiment_outputs_comparison_and_timing_fields(tmp_path: Path, monkeypatch):
    model_ckpt = tmp_path / "model.keras"
    model_ckpt.write_text("stub", encoding="utf-8")
    ptq_tflite = tmp_path / "ptq.tflite"
    ptq_tflite.write_bytes(b"ptq")
    qat_tflite = tmp_path / "qat.tflite"
    qat_tflite.write_bytes(b"qat")

    fp32_metrics_path = tmp_path / "fp32.json"
    fp32_metrics = {
        "accuracy": 0.9,
        "macro_f1": 0.89,
        "confusion_plot": str(tmp_path / "fp32_cm.png"),
        "classification_report": {},
    }
    fp32_metrics_path.write_text(json.dumps(fp32_metrics), encoding="utf-8")

    ptq_report_path = tmp_path / "ptq_report.json"
    ptq_report_path.write_text(
        json.dumps(
            {
                "status": "ok",
                "full_integer_io": True,
                "tflm_compatible": True,
                "unsupported_ops": [],
                "ptq_tflite_size_kb": 12.3,
            }
        ),
        encoding="utf-8",
    )

    qat_report_path = tmp_path / "qat_report.json"
    qat_report_path.write_text(
        json.dumps(
            {
                "status": "ok",
                "full_integer_io": True,
                "tflm_compatible": True,
                "unsupported_ops": [],
            }
        ),
        encoding="utf-8",
    )

    ptq_eval_path = tmp_path / "ptq_eval.json"
    ptq_eval_path.write_text(
        json.dumps(
            {
                "accuracy": 0.88,
                "macro_f1": 0.87,
                "model_size_kb": 12.3,
                "inference_latency_ms_median": 0.4,
                "inference_latency_ms_p95": 0.6,
                "confusion_plot": str(tmp_path / "ptq_cm.png"),
                "classification_report": {},
            }
        ),
        encoding="utf-8",
    )
    qat_eval_path = tmp_path / "qat_eval.json"
    qat_eval_path.write_text(
        json.dumps(
            {
                "accuracy": 0.885,
                "macro_f1": 0.875,
                "model_size_kb": 13.1,
                "inference_latency_ms_median": 0.45,
                "inference_latency_ms_p95": 0.65,
                "confusion_plot": str(tmp_path / "qat_cm.png"),
                "classification_report": {},
            }
        ),
        encoding="utf-8",
    )

    hist_path = tmp_path / "history_fp32.json"
    hist_path.write_text(json.dumps({"loss": [1.0, 0.8], "val_loss": [1.1, 0.9], "accuracy": [0.7, 0.8], "val_accuracy": [0.68, 0.79]}), encoding="utf-8")
    qat_hist_path = tmp_path / "history_qat.json"
    qat_hist_path.write_text(json.dumps({"loss": [0.7, 0.6], "val_loss": [0.75, 0.64], "accuracy": [0.8, 0.84], "val_accuracy": [0.79, 0.83]}), encoding="utf-8")

    monkeypatch.setattr(
        runner,
        "_builder_registry",
        lambda: {
            "xtinyhar_student": (
                lambda **kwargs: None,
                lambda model, learning_rate=1e-4: model,
                {"learning_rate": 1e-4},
            )
        },
    )
    monkeypatch.setattr(
        runner,
        "_export_fp32_tflite_from_checkpoint",
        lambda _ckpt, out_path: (
            Path(out_path).parent.mkdir(parents=True, exist_ok=True),
            Path(out_path).write_bytes(b"fp32"),
            float(Path(out_path).stat().st_size / 1024.0),
        )[-1],
    )
    monkeypatch.setattr(
        runner,
        "runtime_device_report",
        lambda cfg: {
            "run_mode": "full_run",
            "resolved_stage_devices": {
                "train": "cpu",
                "eval_fp32": "cpu",
                "ptq": "cpu",
                "eval_ptq": "cpu",
                "qat": "cpu",
                "eval_qat": "cpu",
            },
        },
    )
    monkeypatch.setattr(runner, "stage_device_scope", lambda cfg, stage: nullcontext())
    monkeypatch.setattr(
        runner.train_model_module,
        "train_model_for_protocol",
        lambda *args, **kwargs: {
            "checkpoint": str(model_ckpt),
            "history_json": str(hist_path),
            "training_time_sec": 2.5,
        },
    )
    monkeypatch.setattr(
        runner.eval_model_module,
        "evaluate_model_for_protocol",
        lambda *args, **kwargs: {"metrics_json": str(fp32_metrics_path), "accuracy": 0.9, "macro_f1": 0.89},
    )
    monkeypatch.setattr(
        runner.ptq_module,
        "quantize_ptq_for_protocol",
        lambda *args, **kwargs: {
            "tflite_model": str(ptq_tflite),
            "report_json": str(ptq_report_path),
            "status": "ok",
        },
    )

    def _fake_eval_tflite(*args, **kwargs):
        tag = kwargs.get("tag", "")
        if "qat" in tag:
            return {"metrics_json": str(qat_eval_path), "accuracy": 0.885, "macro_f1": 0.875}
        return {"metrics_json": str(ptq_eval_path), "accuracy": 0.88, "macro_f1": 0.87}

    monkeypatch.setattr(runner.eval_tflite_module, "evaluate_tflite", _fake_eval_tflite)
    monkeypatch.setattr(
        runner.qat_module,
        "qat_for_protocol",
        lambda *args, **kwargs: {
            "report_json": str(qat_report_path),
            "tflite": str(qat_tflite),
            "status": "ok",
            "history_json": str(qat_hist_path),
            "training_time_sec": 1.1,
        },
    )
    monkeypatch.setattr(
        runner.reporting_module,
        "export_paper_results",
        lambda *args, **kwargs: {"csv": str(tmp_path / "paper.csv"), "md": str(tmp_path / "paper.md")},
    )
    monkeypatch.setattr(
        runner.reporting_module,
        "append_master_results",
        lambda *args, **kwargs: {"csv": str(tmp_path / "master.csv"), "md": str(tmp_path / "master.md")},
    )
    monkeypatch.setattr(
        runner.paper_comparison_module,
        "export_paper_comparison",
        lambda *args, **kwargs: {
            "csv": str(tmp_path / "cmp.csv"),
            "md": str(tmp_path / "cmp.md"),
            "accuracy_png": str(tmp_path / "cmp_acc.png"),
            "size_png": str(tmp_path / "cmp_size.png"),
            "latency_png": str(tmp_path / "cmp_lat.png"),
        },
    )

    cfg = {
        "paths": {"reports_dir": str(tmp_path), "models_tflite_dir": str(tmp_path / "models_tflite")},
        "seed": 42,
        "window_size_default": 200,
        "paper_protocol": {"wisdm_window_override": 200},
        "split_protocols": ["random_stratified"],
        "train": {"learning_rate": 1e-4},
        "quant": {"qat": {"enabled": True, "annotation_policy": "auto"}},
        "experiment": {
            "paper_slug": "xtinyhar",
            "model_variant": "xtinyhar_student",
            "run_id": "r0",
            "compression_focus": "ptq_qat_only",
            "paper_targets": {
                "fp32_accuracy": None,
                "ptq_accuracy": None,
                "qat_accuracy": None,
                "notes": "test",
            },
        },
    }
    out = run_paper_experiment(cfg)
    assert "comparison_exports" in out
    row = out["rows"][0]
    assert "fp32_training_time_sec" in row
    assert "fp32_model_size_kb" in row
    assert row["fp32_model_size_kb"] is not None
    assert row["fp32_tflite_status"] == "ok"
    assert row["fp32_tflite_error"] is None
    assert "ptq_inference_latency_ms_median" in row
    assert "qat_inference_latency_ms_p95" in row
    assert "fp32_curve_png" in row
    assert "qat_curve_png" in row
    assert row["eval_fp32_device"] == "cpu"
    assert row["eval_qat_device"] == "cpu"


def test_run_paper_experiment_continues_when_qat_failed(tmp_path: Path, monkeypatch):
    model_ckpt = tmp_path / "model.keras"
    model_ckpt.write_text("stub", encoding="utf-8")
    ptq_tflite = tmp_path / "ptq.tflite"
    ptq_tflite.write_bytes(b"ptq")

    fp32_metrics_path = tmp_path / "fp32.json"
    fp32_metrics_path.write_text(
        json.dumps(
            {
                "accuracy": 0.91,
                "macro_f1": 0.90,
                "confusion_plot": str(tmp_path / "fp32_cm.png"),
                "classification_report": {},
            }
        ),
        encoding="utf-8",
    )

    ptq_report_path = tmp_path / "ptq_report.json"
    ptq_report_path.write_text(
        json.dumps(
            {
                "status": "ok",
                "full_integer_io": True,
                "tflm_compatible": True,
                "unsupported_ops": [],
            }
        ),
        encoding="utf-8",
    )

    ptq_eval_path = tmp_path / "ptq_eval.json"
    ptq_eval_path.write_text(
        json.dumps(
            {
                "accuracy": 0.89,
                "macro_f1": 0.88,
                "model_size_kb": 11.1,
                "inference_latency_ms_median": 0.3,
                "inference_latency_ms_p95": 0.5,
                "confusion_plot": str(tmp_path / "ptq_cm.png"),
                "classification_report": {},
            }
        ),
        encoding="utf-8",
    )

    qat_report_path = tmp_path / "qat_report_failed.json"
    qat_report_path.write_text(
        json.dumps(
            {
                "status": "failed",
                "full_integer_io": False,
                "tflm_compatible": False,
                "unsupported_ops": [],
                "error": "Conv1D/SeparableConv1D not supported; use *_conv2d",
            }
        ),
        encoding="utf-8",
    )

    hist_path = tmp_path / "history_fp32.json"
    hist_path.write_text(
        json.dumps(
            {
                "loss": [1.0, 0.8],
                "val_loss": [1.1, 0.9],
                "accuracy": [0.7, 0.8],
                "val_accuracy": [0.68, 0.79],
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        runner,
        "_builder_registry",
        lambda: {
            "xtinyhar_student_conv2d": (
                lambda **kwargs: None,
                lambda model, learning_rate=1e-4: model,
                {"learning_rate": 1e-4},
            )
        },
    )
    monkeypatch.setattr(
        runner,
        "_export_fp32_tflite_from_checkpoint",
        lambda _ckpt, out_path: (
            Path(out_path).parent.mkdir(parents=True, exist_ok=True),
            Path(out_path).write_bytes(b"fp32"),
            float(Path(out_path).stat().st_size / 1024.0),
        )[-1],
    )
    monkeypatch.setattr(
        runner,
        "runtime_device_report",
        lambda cfg: {
            "run_mode": "full_run",
            "resolved_stage_devices": {
                "train": "cpu",
                "eval_fp32": "cpu",
                "ptq": "cpu",
                "eval_ptq": "cpu",
                "qat": "cpu",
                "eval_qat": "cpu",
            },
        },
    )
    monkeypatch.setattr(runner, "stage_device_scope", lambda cfg, stage: nullcontext())
    monkeypatch.setattr(
        runner.train_model_module,
        "train_model_for_protocol",
        lambda *args, **kwargs: {
            "checkpoint": str(model_ckpt),
            "history_json": str(hist_path),
            "training_time_sec": 2.0,
        },
    )
    monkeypatch.setattr(
        runner.eval_model_module,
        "evaluate_model_for_protocol",
        lambda *args, **kwargs: {"metrics_json": str(fp32_metrics_path), "accuracy": 0.91, "macro_f1": 0.90},
    )
    monkeypatch.setattr(
        runner.ptq_module,
        "quantize_ptq_for_protocol",
        lambda *args, **kwargs: {
            "tflite_model": str(ptq_tflite),
            "report_json": str(ptq_report_path),
            "status": "ok",
        },
    )
    monkeypatch.setattr(
        runner.eval_tflite_module,
        "evaluate_tflite",
        lambda *args, **kwargs: {
            "metrics_json": str(ptq_eval_path),
            "accuracy": 0.89,
            "macro_f1": 0.88,
        },
    )
    monkeypatch.setattr(
        runner.qat_module,
        "qat_for_protocol",
        lambda *args, **kwargs: {
            "report_json": str(qat_report_path),
            "tflite": str(tmp_path / "missing_qat.tflite"),
            "status": "failed",
            "history_json": None,
            "training_time_sec": None,
        },
    )
    monkeypatch.setattr(
        runner.reporting_module,
        "export_paper_results",
        lambda *args, **kwargs: {"csv": str(tmp_path / "paper.csv"), "md": str(tmp_path / "paper.md")},
    )
    monkeypatch.setattr(
        runner.reporting_module,
        "append_master_results",
        lambda *args, **kwargs: {"csv": str(tmp_path / "master.csv"), "md": str(tmp_path / "master.md")},
    )
    monkeypatch.setattr(
        runner.paper_comparison_module,
        "export_paper_comparison",
        lambda *args, **kwargs: {
            "csv": str(tmp_path / "cmp.csv"),
            "md": str(tmp_path / "cmp.md"),
            "accuracy_png": str(tmp_path / "cmp_acc.png"),
            "size_png": str(tmp_path / "cmp_size.png"),
            "latency_png": str(tmp_path / "cmp_lat.png"),
        },
    )

    cfg = {
        "paths": {"reports_dir": str(tmp_path), "models_tflite_dir": str(tmp_path / "models_tflite")},
        "seed": 42,
        "window_size_default": 200,
        "paper_protocol": {"wisdm_window_override": 200},
        "split_protocols": ["random_stratified"],
        "train": {"learning_rate": 1e-4},
        "quant": {"qat": {"enabled": True, "annotation_policy": "auto"}},
        "experiment": {
            "paper_slug": "xtinyhar",
            "model_variant": "xtinyhar_student_conv2d",
            "run_id": "r0",
            "compression_focus": "ptq_qat_only",
            "paper_targets": {
                "fp32_accuracy": None,
                "ptq_accuracy": None,
                "qat_accuracy": None,
                "notes": "test",
            },
        },
    }
    out = run_paper_experiment(cfg)
    row = out["rows"][0]
    assert "fp32_model_size_kb" in row
    assert row["fp32_model_size_kb"] is not None
    assert row["fp32_tflite_status"] == "ok"
    assert row["qat_status"] == "failed"
    assert row["qat_accuracy"] is None
    assert row["ptq_accuracy"] == pytest.approx(0.89)


def test_run_paper_experiment_continues_when_fp32_tflite_export_failed(tmp_path: Path, monkeypatch):
    model_ckpt = tmp_path / "model.keras"
    model_ckpt.write_text("stub", encoding="utf-8")
    ptq_tflite = tmp_path / "ptq.tflite"
    ptq_tflite.write_bytes(b"ptq")

    fp32_metrics_path = tmp_path / "fp32.json"
    fp32_metrics_path.write_text(
        json.dumps(
            {
                "accuracy": 0.92,
                "macro_f1": 0.91,
                "confusion_plot": str(tmp_path / "fp32_cm.png"),
                "classification_report": {},
            }
        ),
        encoding="utf-8",
    )

    ptq_report_path = tmp_path / "ptq_report.json"
    ptq_report_path.write_text(
        json.dumps(
            {
                "status": "ok",
                "full_integer_io": True,
                "tflm_compatible": True,
                "unsupported_ops": [],
            }
        ),
        encoding="utf-8",
    )

    ptq_eval_path = tmp_path / "ptq_eval.json"
    ptq_eval_path.write_text(
        json.dumps(
            {
                "accuracy": 0.9,
                "macro_f1": 0.89,
                "model_size_kb": 10.5,
                "inference_latency_ms_median": 0.25,
                "inference_latency_ms_p95": 0.4,
                "confusion_plot": str(tmp_path / "ptq_cm.png"),
                "classification_report": {},
            }
        ),
        encoding="utf-8",
    )

    hist_path = tmp_path / "history_fp32.json"
    hist_path.write_text(
        json.dumps(
            {
                "loss": [1.0, 0.8],
                "val_loss": [1.1, 0.9],
                "accuracy": [0.7, 0.8],
                "val_accuracy": [0.68, 0.79],
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        runner,
        "_builder_registry",
        lambda: {
            "xtinyhar_student_conv2d": (
                lambda **kwargs: None,
                lambda model, learning_rate=1e-4: model,
                {"learning_rate": 1e-4},
            )
        },
    )
    monkeypatch.setattr(
        runner,
        "_export_fp32_tflite_from_checkpoint",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(RuntimeError("fp32 tflite export failed")),
    )
    monkeypatch.setattr(
        runner,
        "runtime_device_report",
        lambda cfg: {
            "run_mode": "full_run",
            "resolved_stage_devices": {
                "train": "cpu",
                "eval_fp32": "cpu",
                "ptq": "cpu",
                "eval_ptq": "cpu",
                "qat": "cpu",
                "eval_qat": "cpu",
            },
        },
    )
    monkeypatch.setattr(runner, "stage_device_scope", lambda cfg, stage: nullcontext())
    monkeypatch.setattr(
        runner.train_model_module,
        "train_model_for_protocol",
        lambda *args, **kwargs: {
            "checkpoint": str(model_ckpt),
            "history_json": str(hist_path),
            "training_time_sec": 2.0,
        },
    )
    monkeypatch.setattr(
        runner.eval_model_module,
        "evaluate_model_for_protocol",
        lambda *args, **kwargs: {"metrics_json": str(fp32_metrics_path), "accuracy": 0.92, "macro_f1": 0.91},
    )
    monkeypatch.setattr(
        runner.ptq_module,
        "quantize_ptq_for_protocol",
        lambda *args, **kwargs: {
            "tflite_model": str(ptq_tflite),
            "report_json": str(ptq_report_path),
            "status": "ok",
        },
    )
    monkeypatch.setattr(
        runner.eval_tflite_module,
        "evaluate_tflite",
        lambda *args, **kwargs: {
            "metrics_json": str(ptq_eval_path),
            "accuracy": 0.9,
            "macro_f1": 0.89,
        },
    )
    monkeypatch.setattr(
        runner.reporting_module,
        "export_paper_results",
        lambda *args, **kwargs: {"csv": str(tmp_path / "paper.csv"), "md": str(tmp_path / "paper.md")},
    )
    monkeypatch.setattr(
        runner.reporting_module,
        "append_master_results",
        lambda *args, **kwargs: {"csv": str(tmp_path / "master.csv"), "md": str(tmp_path / "master.md")},
    )
    monkeypatch.setattr(
        runner.paper_comparison_module,
        "export_paper_comparison",
        lambda *args, **kwargs: {
            "csv": str(tmp_path / "cmp.csv"),
            "md": str(tmp_path / "cmp.md"),
            "accuracy_png": str(tmp_path / "cmp_acc.png"),
            "size_png": str(tmp_path / "cmp_size.png"),
            "latency_png": str(tmp_path / "cmp_lat.png"),
        },
    )

    cfg = {
        "paths": {"reports_dir": str(tmp_path), "models_tflite_dir": str(tmp_path / "models_tflite")},
        "seed": 42,
        "window_size_default": 200,
        "paper_protocol": {"wisdm_window_override": 200},
        "split_protocols": ["random_stratified"],
        "train": {"learning_rate": 1e-4},
        "quant": {"qat": {"enabled": False, "annotation_policy": "auto"}},
        "experiment": {
            "paper_slug": "xtinyhar",
            "model_variant": "xtinyhar_student_conv2d",
            "run_id": "r0",
            "compression_focus": "ptq_qat_only",
            "paper_targets": {
                "fp32_accuracy": None,
                "ptq_accuracy": None,
                "qat_accuracy": None,
                "notes": "test",
            },
        },
    }
    out = run_paper_experiment(cfg)
    row = out["rows"][0]
    assert row["fp32_tflite_status"] == "failed"
    assert row["fp32_model_size_kb"] is None
    assert "fp32 tflite export failed" in str(row["fp32_tflite_error"])
    assert row["ptq_accuracy"] == pytest.approx(0.9)
