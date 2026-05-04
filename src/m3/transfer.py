"""Milestone 3 cross-domain transfer experiment runner."""

from __future__ import annotations

import copy
import time
from pathlib import Path
from typing import Any, Callable

import numpy as np
import tensorflow as tf

from src.data.build_dataset import build_dataset_for_protocol
from src.data.io import dataset_exists, load_split_arrays
from src.eval import eval_tflite as eval_tflite_module
from src.eval import evaluate_model as eval_model_module
from src.eval import reporting as reporting_module
from src.eval.plots import save_training_curves
from src.models.serialization import load_checkpoint_model
from src.quant import ptq_full_int8 as ptq_module
from src.quant import qat_train as qat_module
from src.run_paper_experiment import (
    _builder_registry,
    _evaluate_fp32_tflite_if_available,
    _export_fp32_tflite_from_checkpoint,
    _fp32_tflite_path,
    _read_json,
    _write_run_artifact,
)
from src.train.augment import build_training_input
from src.train import train_model as train_model_module
from src.train.train_model import _compile_model
from src.utils import artifacts as artifacts_module
from src.utils.artifacts import model_ckpt_path, model_history_path, norm_stats_path
from src.utils.config import ensure_path_dirs
from src.utils.device_runtime import runtime_device_report, stage_device_scope
from src.utils.repro import dump_json, set_global_seed


CompileFn = Callable[[tf.keras.Model], tf.keras.Model]


def _with_processed_subdir(cfg: dict[str, Any], tag: str, domain: str) -> dict[str, Any]:
    out = copy.deepcopy(cfg)
    paths = out.setdefault("paths", {})
    paths["processed_dir"] = str(Path(paths["processed_dir"]) / f"{tag}_{domain}")
    raw_key = f"{domain}_raw_csv"
    if paths.get(raw_key):
        paths["raw_csv"] = paths[raw_key]

    data = out.setdefault("data", {})
    data["source"] = domain
    data["train_domain"] = domain
    data["eval_domain"] = domain
    return out


def _build_or_rebuild_dataset(
    cfg: dict[str, Any],
    *,
    window_size: int,
    protocol: str,
    normalization_stats: dict[str, Any] | None = None,
    normalization_stats_source: str | None = None,
) -> dict[str, Any]:
    # Transfer datasets encode cross-domain normalization policy. Rebuild them
    # explicitly so a stale local-normalized target dataset cannot be reused.
    return build_dataset_for_protocol(
        cfg,
        window_size=window_size,
        protocol=protocol,
        normalization_stats=normalization_stats,
        normalization_stats_source=normalization_stats_source,
    )


def _norm_stats_for(cfg: dict[str, Any], window_size: int, protocol: str) -> dict[str, Any]:
    return _read_json(norm_stats_path(cfg["paths"]["processed_dir"], window_size, protocol))


def _compile_spec(cfg: dict[str, Any], compile_fn: Callable[..., Any], default_lr: float) -> CompileFn:
    return lambda model: compile_fn(  # noqa: E731
        model,
        learning_rate=float(cfg.get("train", {}).get("learning_rate", default_lr)),
    )


def _finetune_checkpoint(
    cfg: dict[str, Any],
    *,
    checkpoint_path: str,
    compile_spec: CompileFn,
    protocol: str,
    window_size: int,
    run_id: str,
) -> dict[str, Any]:
    ensure_path_dirs(cfg)
    set_global_seed(int(cfg.get("seed", 42)))

    processed_dir = cfg["paths"]["processed_dir"]
    if not dataset_exists(processed_dir, window_size, protocol):
        build_dataset_for_protocol(cfg, window_size, protocol)

    arrays = load_split_arrays(processed_dir, window_size, protocol)
    X_train, y_train = arrays["X_train"], arrays["y_train"]
    X_val, y_val = arrays["X_val"], arrays["y_val"]

    num_classes = len(cfg.get("classes", [])) or int(np.max(y_train)) + 1
    model = load_checkpoint_model(checkpoint_path, compile=False)
    model = _compile_model(model, compile_spec)
    y_train_oh = tf.keras.utils.to_categorical(y_train, num_classes=num_classes)
    y_val_oh = tf.keras.utils.to_categorical(y_val, num_classes=num_classes)

    callbacks = [
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=float(cfg.get("train", {}).get("reduce_lr_factor", 0.5)),
            patience=int(cfg.get("train", {}).get("reduce_lr_patience", 5)),
            verbose=1,
        ),
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=int(cfg.get("train", {}).get("early_stopping_patience", 10)),
            restore_best_weights=True,
            verbose=1,
        ),
    ]

    train_input = build_training_input(
        cfg,
        X_train,
        y_train_oh,
        processed_dir=processed_dir,
        window_size=window_size,
        protocol=protocol,
        batch_size=int(cfg.get("train", {}).get("batch_size", 64)),
    )

    t0 = time.perf_counter()
    history = model.fit(
        *train_input.fit_args(),
        validation_data=(X_val, y_val_oh),
        epochs=int(cfg.get("train", {}).get("epochs", 50)),
        callbacks=callbacks,
        verbose=2,
        **train_input.fit_kwargs,
    )
    training_time_sec = float(time.perf_counter() - t0)

    model_name = str(cfg.get("experiment", {}).get("model_variant", model.name))
    ckpt = model_ckpt_path(
        cfg["paths"]["checkpoints_dir"],
        model_name=model_name,
        window_size=window_size,
        protocol=protocol,
        run_id=run_id,
    )
    hist_path = model_history_path(
        cfg["paths"]["checkpoints_dir"],
        model_name=model_name,
        window_size=window_size,
        protocol=protocol,
        run_id=run_id,
    )
    ckpt.parent.mkdir(parents=True, exist_ok=True)
    model.save(ckpt)
    dump_json(hist_path, history.history)

    return {
        "model_name": model_name,
        "run_id": run_id,
        "checkpoint": str(ckpt),
        "history": str(hist_path),
        "history_json": str(hist_path),
        "epochs_ran": int(len(history.history.get("loss", []))),
        "final_val_accuracy": float(history.history.get("val_accuracy", [0.0])[-1]),
        "training_time_sec": training_time_sec,
        "source_checkpoint": str(checkpoint_path),
    }


def _maybe_export_fp32_tflite(
    *,
    cfg: dict[str, Any],
    model_variant: str,
    window_size: int,
    protocol: str,
    run_id: str,
    checkpoint_path: str,
) -> tuple[Path, float | None, str, str | None]:
    fp32_tflite_model = _fp32_tflite_path(
        models_dir=cfg["paths"]["models_tflite_dir"],
        model_name=model_variant,
        window_size=window_size,
        protocol=protocol,
        run_id=run_id,
    )
    try:
        size_kb = _export_fp32_tflite_from_checkpoint(checkpoint_path, fp32_tflite_model)
        return fp32_tflite_model, size_kb, "ok", None
    except Exception as exc:  # pragma: no cover - runtime converter guarded in Slurm
        return fp32_tflite_model, None, "failed", str(exc)


def _run_quant_and_eval(
    *,
    quant_cfg: dict[str, Any],
    eval_cfg: dict[str, Any],
    model_variant: str,
    checkpoint_path: str,
    window_size: int,
    protocol: str,
    run_id: str,
    paper_reports_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any] | None, dict[str, Any] | None, dict[str, Any] | None]:
    with stage_device_scope(quant_cfg, "ptq"):
        ptq_out = ptq_module.quantize_ptq_for_protocol(
            quant_cfg,
            window_size,
            protocol,
            model_name=model_variant,
            checkpoint_path=checkpoint_path,
            run_id=run_id,
            raise_on_strict_failure=False,
            reports_dir_override=paper_reports_dir,
        )
    ptq_report = _read_json(ptq_out["report_json"])

    with stage_device_scope(eval_cfg, "eval_ptq"):
        ptq_eval = eval_tflite_module.evaluate_tflite(
            eval_cfg,
            ptq_out["tflite_model"],
            window_size,
            protocol,
            tag=f"ptq_{model_variant}_{run_id}",
            reports_dir_override=paper_reports_dir,
    )
    ptq_eval_metrics = _read_json(ptq_eval["metrics_json"])
    ptq_eval_metrics["metrics_json"] = ptq_eval["metrics_json"]

    qat_out = None
    qat_report = None
    qat_eval_metrics = None
    if bool(quant_cfg.get("quant", {}).get("qat", {}).get("enabled", True)):
        with stage_device_scope(quant_cfg, "qat"):
            qat_out = qat_module.qat_for_protocol(
                quant_cfg,
                window_size,
                protocol,
                model_name=model_variant,
                checkpoint_path=checkpoint_path,
                run_id=run_id,
                annotation_policy=quant_cfg.get("quant", {}).get("qat", {}).get(
                    "annotation_policy", "auto"
                ),
                raise_on_strict_failure=False,
                reports_dir_override=paper_reports_dir,
            )
        qat_report = _read_json(qat_out["report_json"])
        if Path(qat_out["tflite"]).exists():
            with stage_device_scope(eval_cfg, "eval_qat"):
                qat_eval = eval_tflite_module.evaluate_tflite(
                    eval_cfg,
                    qat_out["tflite"],
                    window_size,
                    protocol,
                    tag=f"qat_{model_variant}_{run_id}",
                    reports_dir_override=paper_reports_dir,
            )
            qat_eval_metrics = _read_json(qat_eval["metrics_json"])
            qat_eval_metrics["metrics_json"] = qat_eval["metrics_json"]

    return ptq_out, ptq_eval_metrics, qat_out, qat_report, qat_eval_metrics


def run_m3_transfer_experiment(cfg: dict[str, Any]) -> dict[str, Any]:
    """Run zero-shot or WISDM-pretrain/Arduino-fine-tune M3 experiment."""

    exp = cfg.get("experiment", {})
    paper_slug = str(exp.get("paper_slug", "m3"))
    model_variant = str(exp.get("model_variant", "deepconv_lstm_conv2d"))
    run_id = str(exp.get("run_id", "m3_transfer_r0"))
    transfer_mode = str(cfg.get("m3", {}).get("transfer_mode"))

    registry = _builder_registry()
    if model_variant not in registry:
        raise ValueError(f"Unsupported model_variant: {model_variant}")
    builder, compile_fn, compile_kwargs = registry[model_variant]
    compile_spec = _compile_spec(cfg, compile_fn, float(compile_kwargs["learning_rate"]))

    window_size = int(cfg.get("paper_protocol", {}).get("wisdm_window_override", cfg["window_size_default"]))
    protocols = cfg.get("split_protocols", ["random_stratified"])
    runtime_report = runtime_device_report(cfg)
    stage_devices = runtime_report["resolved_stage_devices"]
    run_mode = runtime_report["run_mode"]

    reports_root = Path(cfg["paths"]["reports_dir"])
    paper_reports_dir = reports_root / paper_slug
    paper_reports_dir.mkdir(parents=True, exist_ok=True)

    all_rows: list[dict[str, Any]] = []
    export_paths: dict[str, dict[str, str]] = {}

    for protocol in protocols:
        if transfer_mode == "zero_shot":
            source_domain = str(cfg.get("data", {}).get("train_domain", "wisdm"))
            target_domain = str(cfg.get("data", {}).get("eval_domain", "arduino"))
            train_cfg = _with_processed_subdir(cfg, "source", source_domain)
            eval_cfg = _with_processed_subdir(cfg, "eval", target_domain)

            _build_or_rebuild_dataset(train_cfg, window_size=window_size, protocol=protocol)
            source_norm = _norm_stats_for(train_cfg, window_size, protocol)
            _build_or_rebuild_dataset(
                eval_cfg,
                window_size=window_size,
                protocol=protocol,
                normalization_stats=source_norm,
                normalization_stats_source=(
                    f"{source_domain}_train:{norm_stats_path(train_cfg['paths']['processed_dir'], window_size, protocol)}"
                ),
            )

            with stage_device_scope(train_cfg, "train"):
                train_out = train_model_module.train_model_for_protocol(
                    train_cfg,
                    model_builder=builder,
                    compile_spec=compile_spec,
                    protocol=protocol,
                    window_size=window_size,
                    run_id=run_id,
                )
            final_train_out = train_out
            quant_cfg = train_cfg
            transfer_notes = (
                f"zero_shot source={source_domain} eval={target_domain}; "
                "target arrays normalized with source train stats"
            )

        elif transfer_mode == "finetune":
            pretrain_domain = str(cfg.get("data", {}).get("pretrain_domain", "wisdm"))
            target_domain = str(cfg.get("data", {}).get("train_domain", "arduino"))
            pretrain_cfg = _with_processed_subdir(cfg, "pretrain", pretrain_domain)
            eval_cfg = _with_processed_subdir(cfg, "finetune", target_domain)

            _build_or_rebuild_dataset(pretrain_cfg, window_size=window_size, protocol=protocol)
            _build_or_rebuild_dataset(eval_cfg, window_size=window_size, protocol=protocol)

            pretrain_run_id = f"{run_id}_pretrain"
            with stage_device_scope(pretrain_cfg, "train"):
                pretrain_out = train_model_module.train_model_for_protocol(
                    pretrain_cfg,
                    model_builder=builder,
                    compile_spec=compile_spec,
                    protocol=protocol,
                    window_size=window_size,
                    run_id=pretrain_run_id,
                )
            with stage_device_scope(eval_cfg, "train"):
                final_train_out = _finetune_checkpoint(
                    eval_cfg,
                    checkpoint_path=pretrain_out["checkpoint"],
                    compile_spec=compile_spec,
                    protocol=protocol,
                    window_size=window_size,
                    run_id=run_id,
                )
            quant_cfg = eval_cfg
            transfer_notes = (
                f"finetune pretrain={pretrain_domain} target={target_domain}; "
                "final normalization fitted on target train split only"
            )
        else:
            raise ValueError(f"Unsupported M3 transfer mode for transfer runner: {transfer_mode}")

        fp32_tflite_model, fp32_model_size_kb, fp32_status, fp32_error = _maybe_export_fp32_tflite(
            cfg=cfg,
            model_variant=model_variant,
            window_size=window_size,
            protocol=protocol,
            run_id=run_id,
            checkpoint_path=final_train_out["checkpoint"],
        )

        fp32_curve_png = save_training_curves(
            final_train_out.get("history_json") or final_train_out.get("history"),
            artifacts_module.model_training_curve_png(
                paper_reports_dir,
                model_name=model_variant,
                window_size=window_size,
                protocol=protocol,
                run_id=run_id,
                tier="fp32",
            ),
            title=f"{model_variant} FP32 Training ({protocol}, T={window_size})",
        )

        with stage_device_scope(eval_cfg, "eval_fp32"):
            fp32_eval = eval_model_module.evaluate_model_for_protocol(
                eval_cfg,
                model_path=final_train_out["checkpoint"],
                protocol=protocol,
                window_size=window_size,
                run_id=run_id,
                reports_dir_override=paper_reports_dir,
            )
        fp32_metrics = _read_json(fp32_eval["metrics_json"])
        with stage_device_scope(eval_cfg, "eval_fp32"):
            (
                fp32_tflite_eval,
                fp32_tflite_eval_metrics,
                fp32_tflite_eval_status,
                fp32_tflite_eval_error,
            ) = _evaluate_fp32_tflite_if_available(
                eval_cfg,
                model_path=fp32_tflite_model,
                window_size=window_size,
                protocol=protocol,
                tag=f"fp32_tflite_{model_variant}_{run_id}",
                reports_dir_override=paper_reports_dir,
            )

        ptq_out, ptq_eval_metrics, qat_out, qat_report, qat_eval_metrics = _run_quant_and_eval(
            quant_cfg=quant_cfg,
            eval_cfg=eval_cfg,
            model_variant=model_variant,
            checkpoint_path=final_train_out["checkpoint"],
            window_size=window_size,
            protocol=protocol,
            run_id=run_id,
            paper_reports_dir=paper_reports_dir,
        )
        ptq_report = _read_json(ptq_out["report_json"])
        qat_status = str(qat_out["status"]) if qat_out else "skipped"

        if qat_out and qat_out.get("history_json"):
            qat_curve_png = save_training_curves(
                qat_out["history_json"],
                artifacts_module.model_training_curve_png(
                    paper_reports_dir,
                    model_name=model_variant,
                    window_size=window_size,
                    protocol=protocol,
                    run_id=run_id,
                    tier="qat",
                ),
                title=f"{model_variant} QAT Training ({protocol}, T={window_size})",
            )
        else:
            qat_curve_png = None

        artifact_payload = {
            "paper_slug": paper_slug,
            "protocol": protocol,
            "variant": model_variant,
            "window_size": window_size,
            "seed": int(cfg.get("seed", 42)),
            "run_id": run_id,
            "transfer_mode": transfer_mode,
            "transfer_notes": transfer_notes,
            "run_mode": run_mode,
            "stage_devices": stage_devices,
            "fp32_training_time_sec": final_train_out.get("training_time_sec"),
            "fp32_tflite_model": str(fp32_tflite_model),
            "fp32_tflite_status": fp32_status,
            "fp32_tflite_error": fp32_error,
            "fp32_tflite_eval_status": fp32_tflite_eval_status,
            "fp32_tflite_eval_error": fp32_tflite_eval_error,
            "fp32_tflite_eval_metrics": fp32_tflite_eval_metrics,
            "fp32_metrics": fp32_metrics,
            "ptq_metrics": ptq_report,
            "ptq_eval_metrics": ptq_eval_metrics,
            "qat_metrics": qat_report,
            "qat_eval_metrics": qat_eval_metrics,
        }
        artifact_json = _write_run_artifact(
            cfg["paths"]["reports_dir"],
            paper_slug=paper_slug,
            protocol=protocol,
            variant=model_variant,
            run_id=run_id,
            payload=artifact_payload,
        )

        row = {
            "paper_slug": paper_slug,
            "protocol": protocol,
            "variant": model_variant,
            "run_id": run_id,
            "window_size": window_size,
            "seed": int(cfg.get("seed", 42)),
            "compression_focus": str(exp.get("compression_focus", "ptq_qat_only")),
            "run_mode": run_mode,
            "train_device": stage_devices["train"],
            "eval_fp32_device": stage_devices["eval_fp32"],
            "ptq_device": stage_devices["ptq"],
            "eval_ptq_device": stage_devices["eval_ptq"],
            "qat_device": stage_devices["qat"],
            "eval_qat_device": stage_devices["eval_qat"],
            "fp32_training_time_sec": final_train_out.get("training_time_sec"),
            "fp32_model_size_kb": fp32_model_size_kb,
            "fp32_tflite_model": str(fp32_tflite_model),
            "fp32_tflite_status": fp32_status,
            "fp32_tflite_error": fp32_error,
            "fp32_tflite_eval_status": fp32_tflite_eval_status,
            "fp32_tflite_eval_error": fp32_tflite_eval_error,
            "fp32_tflite_accuracy": (
                float(fp32_tflite_eval["accuracy"]) if fp32_tflite_eval else None
            ),
            "fp32_tflite_macro_f1": (
                float(fp32_tflite_eval["macro_f1"]) if fp32_tflite_eval else None
            ),
            "fp32_tflite_model_size_kb": (
                float(fp32_tflite_eval_metrics["model_size_kb"])
                if fp32_tflite_eval_metrics and fp32_tflite_eval_metrics.get("model_size_kb") is not None
                else None
            ),
            "fp32_tflite_input_dtype": (
                fp32_tflite_eval_metrics.get("input_dtype") if fp32_tflite_eval_metrics else None
            ),
            "fp32_tflite_output_dtype": (
                fp32_tflite_eval_metrics.get("output_dtype") if fp32_tflite_eval_metrics else None
            ),
            "fp32_tflite_inference_latency_ms_mean": (
                fp32_tflite_eval_metrics.get("inference_latency_ms_mean") if fp32_tflite_eval_metrics else None
            ),
            "fp32_tflite_inference_latency_ms_median": (
                fp32_tflite_eval_metrics.get("inference_latency_ms_median") if fp32_tflite_eval_metrics else None
            ),
            "fp32_tflite_inference_latency_ms_p95": (
                fp32_tflite_eval_metrics.get("inference_latency_ms_p95") if fp32_tflite_eval_metrics else None
            ),
            "qat_training_time_sec": qat_out.get("training_time_sec") if qat_out else None,
            "accuracy": float(fp32_eval["accuracy"]),
            "macro_f1": float(fp32_eval["macro_f1"]),
            "ptq_status": str(ptq_out["status"]),
            "qat_status": qat_status,
            "ptq_allowed_ops_profile": ptq_report.get("allowed_ops_profile"),
            "qat_allowed_ops_profile": qat_report.get("allowed_ops_profile") if qat_report else None,
            "ptq_accuracy": float(ptq_eval_metrics["accuracy"]),
            "ptq_macro_f1": float(ptq_eval_metrics["macro_f1"]),
            "qat_accuracy": float(qat_eval_metrics["accuracy"]) if qat_eval_metrics else None,
            "qat_macro_f1": float(qat_eval_metrics["macro_f1"]) if qat_eval_metrics else None,
            "ptq_model_size_kb": (
                float(ptq_eval_metrics["model_size_kb"])
                if ptq_eval_metrics.get("model_size_kb") is not None
                else None
            ),
            "qat_model_size_kb": (
                float(qat_eval_metrics["model_size_kb"])
                if qat_eval_metrics and qat_eval_metrics.get("model_size_kb") is not None
                else None
            ),
            "model_size_kb": (
                float(ptq_eval_metrics["model_size_kb"])
                if ptq_eval_metrics.get("model_size_kb") is not None
                else None
            ),
            "ptq_inference_latency_ms_mean": ptq_eval_metrics.get("inference_latency_ms_mean"),
            "ptq_inference_latency_ms_median": ptq_eval_metrics.get("inference_latency_ms_median"),
            "ptq_inference_latency_ms_p95": ptq_eval_metrics.get("inference_latency_ms_p95"),
            "qat_inference_latency_ms_mean": (
                qat_eval_metrics.get("inference_latency_ms_mean") if qat_eval_metrics else None
            ),
            "qat_inference_latency_ms_median": (
                qat_eval_metrics.get("inference_latency_ms_median") if qat_eval_metrics else None
            ),
            "qat_inference_latency_ms_p95": (
                qat_eval_metrics.get("inference_latency_ms_p95") if qat_eval_metrics else None
            ),
            "fp32_history_json": final_train_out.get("history_json") or final_train_out.get("history"),
            "qat_history_json": qat_out.get("history_json") if qat_out else None,
            "fp32_curve_png": fp32_curve_png,
            "qat_curve_png": qat_curve_png,
            "fp32_confusion_plot": fp32_metrics.get("confusion_plot"),
            "fp32_tflite_confusion_plot": (
                fp32_tflite_eval_metrics.get("confusion_plot") if fp32_tflite_eval_metrics else None
            ),
            "ptq_confusion_plot": ptq_eval_metrics.get("confusion_plot"),
            "qat_confusion_plot": qat_eval_metrics.get("confusion_plot") if qat_eval_metrics else None,
            "paper_target_score": None,
            "delta_vs_paper": None,
            "notes_assumptions": transfer_notes,
            "transfer_notes": transfer_notes,
            "fp32_metrics_json": fp32_eval["metrics_json"],
            "fp32_tflite_metrics_json": (
                fp32_tflite_eval_metrics.get("metrics_json") if fp32_tflite_eval_metrics else None
            ),
            "ptq_metrics_json": ptq_eval_metrics.get("metrics_json"),
            "qat_metrics_json": qat_eval_metrics.get("metrics_json") if qat_eval_metrics else None,
            "ptq_report_json": ptq_out["report_json"],
            "qat_report_json": qat_out["report_json"] if qat_out else None,
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
    from src.m3 import reporting as m3_reporting

    m3_master_paths = m3_reporting.append_m3_results(cfg["paths"]["reports_dir"], cfg, all_rows)
    return {
        "paper_slug": paper_slug,
        "rows": all_rows,
        "paper_exports": export_paths,
        "master_exports": master_paths,
        "m3_master_exports": m3_master_paths,
    }
