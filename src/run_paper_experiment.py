"""Run a paper model end-to-end on WISDM with standardized reporting."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from src.eval import eval_tflite as eval_tflite_module
from src.eval import evaluate_model as eval_model_module
from src.eval import paper_comparison as paper_comparison_module
from src.eval import reporting as reporting_module
from src.eval.plots import save_training_curves
from src.models import (
    build_daghero_2layer,
    build_daghero_2layer_conv2d,
    build_daghero_4layer,
    build_daghero_4layer_conv2d,
    build_repmobile_folded,
    build_repmobile_folded_conv2d,
    build_tahar_student_cnn,
    build_tahar_student_gru,
    build_tahar_student_lstm,
    build_tcn_attention_har_teacher,
    build_tcn_attention_har_teacher_conv2d,
    build_tcn_inception,
    build_tcn_inception_conv2d,
    build_xtinyhar_student,
    build_xtinyhar_student_conv2d,
    compile_daghero_cnn,
    compile_repmobile_folded,
    compile_tcn_attention,
    compile_tcn_inception,
    compile_xtinyhar_student,
)
from src.quant import ptq_full_int8 as ptq_module
from src.quant import qat_train as qat_module
from src.train import train_model as train_model_module
from src.utils.artifacts import model_training_curve_png
from src.utils.config import apply_common_overrides, build_parser, load_yaml
from src.utils.device_runtime import runtime_device_report, stage_device_scope


Builder = Callable[..., Any]


def _read_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def _builder_registry() -> dict[str, tuple[Builder, Callable[[Any], Any], dict[str, Any]]]:
    return {
        "xtinyhar_student": (
            build_xtinyhar_student,
            compile_xtinyhar_student,
            {"learning_rate": 1e-4},
        ),
        "xtinyhar_student_conv2d": (
            build_xtinyhar_student_conv2d,
            compile_xtinyhar_student,
            {"learning_rate": 1e-4},
        ),
        "repmobile_folded": (
            build_repmobile_folded,
            compile_repmobile_folded,
            {"learning_rate": 1e-4},
        ),
        "repmobile_folded_conv2d": (
            build_repmobile_folded_conv2d,
            compile_repmobile_folded,
            {"learning_rate": 1e-4},
        ),
        "tcn_attention_har_teacher": (
            build_tcn_attention_har_teacher,
            compile_tcn_attention,
            {"learning_rate": 5e-4},
        ),
        "tcn_attention_har_teacher_conv2d": (
            build_tcn_attention_har_teacher_conv2d,
            compile_tcn_attention,
            {"learning_rate": 5e-4},
        ),
        "tahar_student_cnn": (
            build_tahar_student_cnn,
            compile_tcn_attention,
            {"learning_rate": 5e-4},
        ),
        "tahar_student_lstm": (
            build_tahar_student_lstm,
            compile_tcn_attention,
            {"learning_rate": 5e-4},
        ),
        "tahar_student_gru": (
            build_tahar_student_gru,
            compile_tcn_attention,
            {"learning_rate": 5e-4},
        ),
        "daghero_cnn_2layer": (
            build_daghero_2layer,
            compile_daghero_cnn,
            {"learning_rate": 1e-3},
        ),
        "daghero_cnn_2layer_conv2d": (
            build_daghero_2layer_conv2d,
            compile_daghero_cnn,
            {"learning_rate": 1e-3},
        ),
        "daghero_cnn_4layer": (
            build_daghero_4layer,
            compile_daghero_cnn,
            {"learning_rate": 1e-3},
        ),
        "daghero_cnn_4layer_conv2d": (
            build_daghero_4layer_conv2d,
            compile_daghero_cnn,
            {"learning_rate": 1e-3},
        ),
        "tcn_inception": (
            build_tcn_inception,
            compile_tcn_inception,
            {"learning_rate": 5e-4},
        ),
        "tcn_inception_conv2d": (
            build_tcn_inception_conv2d,
            compile_tcn_inception,
            {"learning_rate": 5e-4},
        ),
    }


def _write_run_artifact(
    reports_dir: str | Path,
    paper_slug: str,
    protocol: str,
    variant: str,
    run_id: str,
    payload: dict[str, Any],
) -> str:
    out_dir = Path(reports_dir) / paper_slug / "artifacts"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{paper_slug}_{variant}_{protocol}_{run_id}.json"
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True)
    return str(out_path)


def run_paper_experiment(cfg: dict[str, Any]) -> dict[str, Any]:
    exp = cfg.get("experiment", {})
    paper_slug = str(exp.get("paper_slug", "unknown_paper"))
    model_variant = str(exp.get("model_variant", "xtinyhar_student"))
    run_id = str(exp.get("run_id", "r0"))
    compression_focus = str(exp.get("compression_focus", "ptq_qat_only")).strip().lower()
    if compression_focus != "ptq_qat_only":
        raise ValueError(
            "This pipeline is restricted to PTQ/QAT compression only. "
            "Set experiment.compression_focus=ptq_qat_only."
        )

    registry = _builder_registry()
    if model_variant not in registry:
        raise ValueError(f"Unsupported model_variant: {model_variant}")

    builder, compile_fn, compile_kwargs = registry[model_variant]
    compile_spec = lambda m: compile_fn(  # noqa: E731
        m,
        learning_rate=float(cfg.get("train", {}).get("learning_rate", compile_kwargs["learning_rate"])),
    )

    window_size = int(cfg.get("paper_protocol", {}).get("wisdm_window_override", cfg["window_size_default"]))
    protocols = cfg.get("split_protocols", ["random_stratified", "user_holdout"])
    runtime_report = runtime_device_report(cfg)
    stage_devices = runtime_report["resolved_stage_devices"]
    run_mode = runtime_report["run_mode"]
    paper_targets = dict(exp.get("paper_targets", {}))
    reports_root = Path(cfg["paths"]["reports_dir"])
    paper_reports_dir = reports_root / paper_slug
    paper_reports_dir.mkdir(parents=True, exist_ok=True)

    all_rows: list[dict[str, Any]] = []
    export_paths: dict[str, dict[str, str]] = {}

    for protocol in protocols:
        with stage_device_scope(cfg, "train"):
            train_out = train_model_module.train_model_for_protocol(
                cfg,
                model_builder=builder,
                compile_spec=compile_spec,
                protocol=protocol,
                window_size=window_size,
                run_id=run_id,
            )
        fp32_curve_png = save_training_curves(
            train_out.get("history_json") or train_out.get("history"),
            model_training_curve_png(
                paper_reports_dir,
                model_name=model_variant,
                window_size=window_size,
                protocol=protocol,
                run_id=run_id,
                tier="fp32",
            ),
            title=f"{model_variant} FP32 Training ({protocol}, T={window_size})",
        )

        with stage_device_scope(cfg, "eval_fp32"):
            fp32_eval = eval_model_module.evaluate_model_for_protocol(
                cfg,
                model_path=train_out["checkpoint"],
                protocol=protocol,
                window_size=window_size,
                run_id=run_id,
                reports_dir_override=paper_reports_dir,
            )
        fp32_metrics = _read_json(fp32_eval["metrics_json"])

        with stage_device_scope(cfg, "ptq"):
            ptq_out = ptq_module.quantize_ptq_for_protocol(
                cfg,
                window_size,
                protocol,
                model_name=model_variant,
                checkpoint_path=train_out["checkpoint"],
                run_id=run_id,
                raise_on_strict_failure=False,
                reports_dir_override=paper_reports_dir,
            )
        ptq_report = _read_json(ptq_out["report_json"])
        with stage_device_scope(cfg, "eval_ptq"):
            ptq_eval = eval_tflite_module.evaluate_tflite(
                cfg,
                ptq_out["tflite_model"],
                window_size,
                protocol,
                tag=f"ptq_{model_variant}_{run_id}",
                reports_dir_override=paper_reports_dir,
            )
        ptq_eval_metrics = _read_json(ptq_eval["metrics_json"])

        qat_eval = None
        qat_eval_metrics = None
        qat_report = {}
        qat_curve_png = None
        qat_status = "skipped"
        qat_out = None
        if bool(cfg.get("quant", {}).get("qat", {}).get("enabled", True)):
            with stage_device_scope(cfg, "qat"):
                qat_out = qat_module.qat_for_protocol(
                    cfg,
                    window_size,
                    protocol,
                    model_name=model_variant,
                    checkpoint_path=train_out["checkpoint"],
                    run_id=run_id,
                    annotation_policy=cfg.get("quant", {}).get("qat", {}).get("annotation_policy", "auto"),
                    raise_on_strict_failure=False,
                    reports_dir_override=paper_reports_dir,
                )
            qat_report = _read_json(qat_out["report_json"])
            qat_status = str(qat_out["status"])
            if qat_out.get("history_json"):
                qat_curve_png = save_training_curves(
                    qat_out["history_json"],
                    model_training_curve_png(
                        paper_reports_dir,
                        model_name=model_variant,
                        window_size=window_size,
                        protocol=protocol,
                        run_id=run_id,
                        tier="qat",
                    ),
                    title=f"{model_variant} QAT Training ({protocol}, T={window_size})",
                )
            if Path(qat_out["tflite"]).exists():
                with stage_device_scope(cfg, "eval_qat"):
                    qat_eval = eval_tflite_module.evaluate_tflite(
                        cfg,
                        qat_out["tflite"],
                        window_size,
                        protocol,
                        tag=f"qat_{model_variant}_{run_id}",
                        reports_dir_override=paper_reports_dir,
                    )
                qat_eval_metrics = _read_json(qat_eval["metrics_json"])

        run_artifact_payload = {
            "paper_slug": paper_slug,
            "protocol": protocol,
            "variant": model_variant,
            "window_size": window_size,
            "seed": int(cfg.get("seed", 42)),
            "run_id": run_id,
            "compression_focus": compression_focus,
            "run_mode": run_mode,
            "train_device": stage_devices["train"],
            "eval_fp32_device": stage_devices["eval_fp32"],
            "ptq_device": stage_devices["ptq"],
            "eval_ptq_device": stage_devices["eval_ptq"],
            "qat_device": stage_devices["qat"],
            "eval_qat_device": stage_devices["eval_qat"],
            "fp32_training_time_sec": train_out.get("training_time_sec"),
            "qat_training_time_sec": qat_out.get("training_time_sec") if qat_out else None,
            "ptq_inference_latency_ms_median": ptq_eval_metrics.get("inference_latency_ms_median"),
            "ptq_inference_latency_ms_p95": ptq_eval_metrics.get("inference_latency_ms_p95"),
            "qat_inference_latency_ms_median": (
                qat_eval_metrics.get("inference_latency_ms_median") if qat_eval_metrics else None
            ),
            "qat_inference_latency_ms_p95": (
                qat_eval_metrics.get("inference_latency_ms_p95") if qat_eval_metrics else None
            ),
            "fp32_history_json": train_out.get("history_json") or train_out.get("history"),
            "qat_history_json": qat_out.get("history_json") if qat_out else None,
            "fp32_curve_png": fp32_curve_png,
            "qat_curve_png": qat_curve_png,
            "fp32_confusion_plot": fp32_metrics.get("confusion_plot"),
            "ptq_confusion_plot": ptq_eval_metrics.get("confusion_plot"),
            "qat_confusion_plot": qat_eval_metrics.get("confusion_plot") if qat_eval_metrics else None,
            "fp32_metrics": fp32_metrics,
            "ptq_metrics": ptq_report,
            "qat_metrics": qat_report if qat_out is not None else None,
            "deploy_gate": {
                "ptq": {
                    "status": ptq_report.get("status"),
                    "full_integer_io": ptq_report.get("full_integer_io"),
                    "tflm_compatible": ptq_report.get("tflm_compatible"),
                    "unsupported_ops": ptq_report.get("unsupported_ops", []),
                },
                "qat": {
                    "status": qat_report.get("status"),
                    "full_integer_io": qat_report.get("full_integer_io"),
                    "tflm_compatible": qat_report.get("tflm_compatible"),
                    "unsupported_ops": qat_report.get("unsupported_ops", []),
                },
            },
        }
        artifact_json = _write_run_artifact(
            cfg["paths"]["reports_dir"],
            paper_slug=paper_slug,
            protocol=protocol,
            variant=model_variant,
            run_id=run_id,
            payload=run_artifact_payload,
        )

        row = {
            "paper_slug": paper_slug,
            "protocol": protocol,
            "variant": model_variant,
            "run_id": run_id,
            "window_size": window_size,
            "seed": int(cfg.get("seed", 42)),
            "compression_focus": compression_focus,
            "run_mode": run_mode,
            "train_device": stage_devices["train"],
            "eval_fp32_device": stage_devices["eval_fp32"],
            "ptq_device": stage_devices["ptq"],
            "eval_ptq_device": stage_devices["eval_ptq"],
            "qat_device": stage_devices["qat"],
            "eval_qat_device": stage_devices["eval_qat"],
            "fp32_training_time_sec": train_out.get("training_time_sec"),
            "qat_training_time_sec": qat_out.get("training_time_sec") if qat_out else None,
            "accuracy": float(fp32_eval["accuracy"]),
            "macro_f1": float(fp32_eval["macro_f1"]),
            "ptq_status": str(ptq_out["status"]),
            "qat_status": qat_status,
            "ptq_accuracy": float(ptq_eval["accuracy"]),
            "ptq_macro_f1": float(ptq_eval_metrics["macro_f1"]),
            "qat_accuracy": float(qat_eval["accuracy"]) if qat_eval else None,
            "qat_macro_f1": float(qat_eval_metrics["macro_f1"]) if qat_eval_metrics else None,
            "ptq_model_size_kb": float(ptq_eval_metrics["model_size_kb"]) if ptq_eval_metrics.get("model_size_kb") is not None else None,
            "qat_model_size_kb": (
                float(qat_eval_metrics["model_size_kb"]) if qat_eval_metrics and qat_eval_metrics.get("model_size_kb") is not None else None
            ),
            "model_size_kb": float(ptq_eval_metrics["model_size_kb"]) if ptq_eval_metrics.get("model_size_kb") is not None else None,
            "ptq_inference_latency_ms_median": ptq_eval_metrics.get("inference_latency_ms_median"),
            "ptq_inference_latency_ms_p95": ptq_eval_metrics.get("inference_latency_ms_p95"),
            "qat_inference_latency_ms_median": (
                qat_eval_metrics.get("inference_latency_ms_median") if qat_eval_metrics else None
            ),
            "qat_inference_latency_ms_p95": (
                qat_eval_metrics.get("inference_latency_ms_p95") if qat_eval_metrics else None
            ),
            "fp32_history_json": train_out.get("history_json") or train_out.get("history"),
            "qat_history_json": qat_out.get("history_json") if qat_out else None,
            "fp32_curve_png": fp32_curve_png,
            "qat_curve_png": qat_curve_png,
            "fp32_confusion_plot": fp32_metrics.get("confusion_plot"),
            "ptq_confusion_plot": ptq_eval_metrics.get("confusion_plot"),
            "qat_confusion_plot": qat_eval_metrics.get("confusion_plot") if qat_eval_metrics else None,
            "deploy_gate": {
                "ptq": {
                    "status": ptq_report.get("status"),
                    "full_integer_io": ptq_report.get("full_integer_io"),
                    "tflm_compatible": ptq_report.get("tflm_compatible"),
                    "unsupported_ops": ptq_report.get("unsupported_ops", []),
                },
                "qat": {
                    "status": qat_report.get("status"),
                    "full_integer_io": qat_report.get("full_integer_io"),
                    "tflm_compatible": qat_report.get("tflm_compatible"),
                    "unsupported_ops": qat_report.get("unsupported_ops", []),
                },
            },
            "paper_target_score": paper_targets.get(
                "fp32_accuracy", cfg.get("experiment", {}).get("paper_target_score")
            ),
            "delta_vs_paper": (
                float(fp32_metrics["accuracy"])
                - float(
                    paper_targets.get(
                        "fp32_accuracy", cfg.get("experiment", {}).get("paper_target_score")
                    )
                )
                if paper_targets.get(
                    "fp32_accuracy", cfg.get("experiment", {}).get("paper_target_score")
                )
                is not None
                else None
            ),
            "notes_assumptions": cfg.get("experiment", {}).get("notes_assumptions"),
            "fp32_metrics_json": fp32_eval["metrics_json"],
            "ptq_metrics_json": ptq_eval["metrics_json"],
            "qat_metrics_json": qat_eval["metrics_json"] if qat_eval else None,
            "ptq_report_json": ptq_out["report_json"],
            "qat_report_json": qat_out["report_json"] if qat_out is not None else None,
            "run_artifact_json": artifact_json,
        }
        all_rows.append(row)

        export_paths[protocol] = reporting_module.export_paper_results(
            cfg["paths"]["reports_dir"],
            paper_slug=paper_slug,
            protocol=protocol,
            rows=[row],
        )

    master_paths = reporting_module.append_master_results(cfg["paths"]["reports_dir"], all_rows)
    comparison_exports = paper_comparison_module.export_paper_comparison(
        cfg["paths"]["reports_dir"],
        paper_slug=paper_slug,
        run_rows=all_rows,
        paper_targets=paper_targets,
    )
    return {
        "paper_slug": paper_slug,
        "rows": all_rows,
        "paper_exports": export_paths,
        "comparison_exports": comparison_exports,
        "master_exports": master_paths,
    }


def main() -> None:
    parser = build_parser("Run a paper model experiment bundle")
    args = parser.parse_args()
    cfg = apply_common_overrides(load_yaml(args.config), args)

    out = run_paper_experiment(cfg)
    print(f"paper_slug: {out['paper_slug']}")
    print(f"rows: {len(out['rows'])}")
    print(f"master_csv: {out['master_exports']['csv']}")
    print(f"master_md: {out['master_exports']['md']}")


if __name__ == "__main__":
    main()
