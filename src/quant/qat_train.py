"""Quantization-aware training with strict deployability reporting."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import numpy as np
import tensorflow as tf

from src.data.build_dataset import build_dataset_for_protocol
from src.data.io import dataset_exists, load_split_arrays
from src.quant.deploy_gate import (
    accepted_integer_dtypes,
    inspect_tflite_and_evaluate_deploy_gate,
    representative_array,
    representative_dataset,
)
from src.train.train_baseline import train_baseline_for_protocol
from src.utils.artifacts import (
    baseline_ckpt_path,
    model_ckpt_path,
    model_qat_history_path,
    model_qat_tflite_path,
    model_slug,
    qat_tflite_path,
    run_prefix,
    variant_suffix,
)
from src.utils.config import apply_common_overrides, build_parser, ensure_path_dirs, load_yaml
from src.utils.repro import dump_json


def _build_qat_model(
    fp32_model: tf.keras.Model,
    annotation_policy: str = "auto",
) -> tuple[tf.keras.Model, str]:
    import tensorflow_model_optimization as tfmot

    policy = str(annotation_policy).strip().lower()
    if policy in {"auto", "full"}:
        try:
            qat_model = tfmot.quantization.keras.quantize_model(fp32_model)
            return qat_model, "quantize_model_full"
        except Exception:
            if policy == "full":
                raise

    quantize_annotate_layer = tfmot.quantization.keras.quantize_annotate_layer
    quantize_apply = tfmot.quantization.keras.quantize_apply

    allowed: set[type[tf.keras.layers.Layer]] = set()
    if policy in {"auto", "conv_dense", "conv1d_dense"}:
        allowed.update({tf.keras.layers.Conv1D, tf.keras.layers.Dense})
    if policy in {"conv2d_dense"}:
        allowed.update({tf.keras.layers.Conv2D, tf.keras.layers.Dense})
    if policy in {"dense_only"}:
        allowed.update({tf.keras.layers.Dense})
    if policy in {"depthwise_conv2d_dense", "depthwise"}:
        allowed.update({tf.keras.layers.DepthwiseConv2D, tf.keras.layers.Dense})
    if policy in {"all_supported"}:
        allowed.update(
            {
                tf.keras.layers.Conv1D,
                tf.keras.layers.Conv2D,
                tf.keras.layers.DepthwiseConv2D,
                tf.keras.layers.Dense,
            }
        )
    if not allowed:
        allowed.update({tf.keras.layers.Conv1D, tf.keras.layers.Dense})

    def annotate(layer: tf.keras.layers.Layer) -> tf.keras.layers.Layer:
        if any(isinstance(layer, t) for t in allowed):
            return quantize_annotate_layer(layer)
        return layer

    annotated = tf.keras.models.clone_model(fp32_model, clone_function=annotate)
    annotated.set_weights(fp32_model.get_weights())
    qat_model = quantize_apply(annotated)
    return qat_model, f"annotate_policy_{policy}"


def _report_paths(
    reports_dir: str | Path,
    model_name: str,
    window_size: int,
    protocol: str,
    run_id: str | None,
    variant: str | None,
) -> tuple[Path, Path]:
    suffix = variant_suffix(variant)
    if model_slug(model_name) == "deepconv_lstm" and not run_id:
        base = f"qat_export_T{window_size}_P{protocol}{suffix}"
    else:
        base = f"qat_export_{run_prefix(model_name, window_size, protocol, run_id)}{suffix}"
    reports_path = Path(reports_dir)
    return reports_path / f"{base}.json", reports_path / f"{base}.md"


def _write_qat_markdown(md_path: Path, metrics: dict[str, Any]) -> None:
    with md_path.open("w", encoding="utf-8") as f:
        f.write(
            f"# QAT Export (T={metrics['window_size']}, protocol={metrics['protocol']}, "
            f"variant={metrics['variant']})\n\n"
        )
        f.write(f"- QAT checkpoint: `{metrics['qat_checkpoint']}`\n")
        if metrics.get("qat_tflite"):
            f.write(f"- QAT tflite: `{metrics['qat_tflite']}`\n")
        f.write(f"- Status: `{metrics['status']}`\n")
        f.write(f"- Deployable full integer: `{metrics['deployable_full_int8']}`\n")
        f.write(f"- Full integer I/O: `{metrics['full_integer_io']}`\n")
        f.write(f"- TFLM compatible: `{metrics['tflm_compatible']}`\n")
        f.write(f"- Input dtype: `{metrics['input_dtype']}`\n")
        f.write(f"- Output dtype: `{metrics['output_dtype']}`\n")
        f.write(f"- Accepted integer I/O dtypes: `{metrics['accepted_integer_io_dtypes']}`\n")
        f.write(f"- Representative source: `{metrics['representative_source']}`\n")
        f.write(f"- Representative samples: `{metrics['representative_samples']}`\n")
        if metrics.get("training_time_sec") is not None:
            f.write(f"- QAT training time: {float(metrics['training_time_sec']):.3f} s\n")
        if metrics.get("history_json"):
            f.write(f"- QAT history JSON: `{metrics['history_json']}`\n")
        if metrics.get("error"):
            f.write(f"- Error: `{metrics['error']}`\n")
        if metrics.get("unsupported_ops"):
            f.write(f"- Unsupported ops: `{', '.join(metrics['unsupported_ops'])}`\n")
        f.write("\n## Notes\n\n")
        for note in metrics.get("notes", []):
            f.write(f"- {note}\n")


def qat_for_protocol(
    cfg: dict[str, Any],
    window_size: int,
    protocol: str,
    *,
    model_name: str = "deepconv_lstm",
    checkpoint_path: str | None = None,
    run_id: str | None = None,
    annotation_policy: str | None = None,
    variant: str | None = None,
    raise_on_strict_failure: bool = True,
    reports_dir_override: str | Path | None = None,
) -> dict[str, Any]:
    ensure_path_dirs(cfg)
    processed_dir = cfg["paths"]["processed_dir"]

    if not dataset_exists(processed_dir, window_size, protocol):
        build_dataset_for_protocol(cfg, window_size, protocol)

    if checkpoint_path is not None:
        ckpt_path = Path(checkpoint_path)
    elif model_slug(model_name) == "deepconv_lstm" and not run_id:
        ckpt_path = baseline_ckpt_path(cfg["paths"]["checkpoints_dir"], window_size, protocol)
    else:
        ckpt_path = model_ckpt_path(
            cfg["paths"]["checkpoints_dir"],
            model_name=model_name,
            window_size=window_size,
            protocol=protocol,
            run_id=run_id,
        )

    if not ckpt_path.exists():
        if model_slug(model_name) == "deepconv_lstm" and checkpoint_path is None and not run_id:
            train_baseline_for_protocol(cfg, window_size, protocol)
        else:
            raise FileNotFoundError(
                f"Checkpoint not found for model '{model_name}'. Provide checkpoint_path or train it first: {ckpt_path}"
            )

    arrays = load_split_arrays(processed_dir, window_size, protocol)
    X_train, y_train = arrays["X_train"], arrays["y_train"]
    X_val, y_val = arrays["X_val"], arrays["y_val"]

    qat_cfg = cfg.get("quant", {}).get("qat", {})
    rep_source = str(qat_cfg.get("representative_source", "train")).strip().lower()
    rep_count = int(
        qat_cfg.get(
            "representative_samples",
            cfg.get("quant", {}).get("ptq", {}).get("representative_samples", 256),
        )
    )
    strict_full_int8 = bool(qat_cfg.get("strict_full_int8", True))
    require_tflm_compatible = bool(qat_cfg.get("require_tflm_compatible", True))
    accepted_io = accepted_integer_dtypes(
        qat_cfg.get("accepted_integer_io_dtypes", ["int8", "uint8"])
    )
    enforce_full_int8 = bool(qat_cfg.get("enforce_full_int8", True)) or strict_full_int8

    ckpt_dir = Path(cfg["paths"]["checkpoints_dir"])
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    variant_suffix_text = variant_suffix(variant)
    if model_slug(model_name) == "deepconv_lstm" and not run_id:
        qat_ckpt = ckpt_dir / f"deepconv_lstm_qat_T{window_size}_P{protocol}{variant_suffix_text}.keras"
        qat_history_path = (
            ckpt_dir / f"history_deepconv_lstm_qat_T{window_size}_P{protocol}{variant_suffix_text}.json"
        )
    else:
        qat_ckpt = (
            ckpt_dir
            / f"{run_prefix(model_name, window_size, protocol, run_id)}_qat{variant_suffix_text}.keras"
        )
        qat_history_path = model_qat_history_path(
            ckpt_dir,
            model_name=model_name,
            window_size=window_size,
            protocol=protocol,
            run_id=run_id,
            variant=variant,
        )

    if model_slug(model_name) == "deepconv_lstm" and not run_id:
        tfl_path = qat_tflite_path(
            cfg["paths"]["models_tflite_dir"], window_size, protocol, variant=variant
        )
    else:
        tfl_path = model_qat_tflite_path(
            cfg["paths"]["models_tflite_dir"],
            model_name=model_name,
            window_size=window_size,
            protocol=protocol,
            run_id=run_id,
            variant=variant,
        )
    tfl_path.parent.mkdir(parents=True, exist_ok=True)

    reports_dir = Path(reports_dir_override) if reports_dir_override else Path(cfg["paths"]["reports_dir"])
    reports_dir.mkdir(parents=True, exist_ok=True)
    json_path, md_path = _report_paths(
        reports_dir,
        model_name=model_name,
        window_size=window_size,
        protocol=protocol,
        run_id=run_id,
        variant=variant,
    )

    num_classes = len(cfg.get("classes", [])) or int(np.max(y_train)) + 1
    y_train_oh = tf.keras.utils.to_categorical(y_train, num_classes)
    y_val_oh = tf.keras.utils.to_categorical(y_val, num_classes)

    fp32_model = tf.keras.models.load_model(ckpt_path)

    notes: list[str] = []
    training_time_sec: float | None = None

    def _emit_failure(error_msg: str, *, epochs_ran: int = 0) -> None:
        payload = {
            "window_size": int(window_size),
            "protocol": protocol,
            "model_name": model_name,
            "run_id": run_id,
            "variant": variant or "default",
            "qat_checkpoint": str(qat_ckpt),
            "qat_tflite": str(tfl_path) if tfl_path.exists() else None,
            "input_dtype": None,
            "output_dtype": None,
            "input_dtype_normalized": None,
            "output_dtype_normalized": None,
            "accepted_integer_io_dtypes": accepted_io,
            "full_integer_io": False,
            "representative_source": rep_source,
            "representative_samples": int(rep_count),
            "strict_full_int8": bool(strict_full_int8),
            "require_tflm_compatible": bool(require_tflm_compatible),
            "deployable_full_int8": False,
            "tflm_compatible": False,
            "unsupported_ops": [],
            "tflm_ops": [],
            "compat_error": None,
            "has_unidirectional_sequence_lstm": False,
            "has_while_op": False,
            "training_time_sec": training_time_sec,
            "history_json": str(qat_history_path) if qat_history_path.exists() else None,
            "epochs_ran": int(epochs_ran),
            "status": "failed",
            "error": error_msg,
            "notes": notes,
        }
        dump_json(json_path, payload)
        _write_qat_markdown(md_path, payload)

    try:
        policy = annotation_policy or str(qat_cfg.get("annotation_policy", "auto"))
        qat_model, strategy = _build_qat_model(fp32_model, annotation_policy=policy)
        notes.append(f"QAT strategy: {strategy}")
    except Exception as exc:
        error_msg = f"Unable to construct QAT model: {exc}"
        notes.append(error_msg)
        _emit_failure(error_msg, epochs_ran=0)
        raise RuntimeError(error_msg) from exc

    qat_model.compile(
        optimizer=tf.keras.optimizers.RMSprop(
            learning_rate=float(qat_cfg.get("learning_rate", 1e-4))
        ),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    train_t0 = time.perf_counter()
    hist = qat_model.fit(
        X_train,
        y_train_oh,
        validation_data=(X_val, y_val_oh),
        epochs=int(qat_cfg.get("epochs", 10)),
        batch_size=int(qat_cfg.get("batch_size", cfg["train"].get("batch_size", 64))),
        verbose=2,
    )
    training_time_sec = float(time.perf_counter() - train_t0)

    qat_model.save(qat_ckpt)
    dump_json(qat_history_path, hist.history)

    try:
        X_rep = representative_array(arrays, rep_source)
    except Exception as exc:
        error_msg = f"Invalid representative source for QAT: {exc}"
        payload = {
            "window_size": int(window_size),
            "protocol": protocol,
            "model_name": model_name,
            "run_id": run_id,
            "variant": variant or "default",
            "qat_checkpoint": str(qat_ckpt),
            "qat_tflite": None,
            "input_dtype": None,
            "output_dtype": None,
            "input_dtype_normalized": None,
            "output_dtype_normalized": None,
            "accepted_integer_io_dtypes": accepted_io,
            "full_integer_io": False,
            "representative_source": rep_source,
            "representative_samples": int(rep_count),
            "strict_full_int8": bool(strict_full_int8),
            "require_tflm_compatible": bool(require_tflm_compatible),
            "deployable_full_int8": False,
            "tflm_compatible": False,
            "unsupported_ops": [],
            "tflm_ops": [],
            "compat_error": None,
            "has_unidirectional_sequence_lstm": False,
            "has_while_op": False,
            "training_time_sec": training_time_sec,
            "history_json": str(qat_history_path),
            "epochs_ran": int(len(hist.history.get("loss", []))),
            "status": "failed",
            "error": error_msg,
            "notes": notes,
        }
        dump_json(json_path, payload)
        _write_qat_markdown(md_path, payload)
        raise RuntimeError(error_msg) from exc

    converter = tf.lite.TFLiteConverter.from_keras_model(qat_model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.representative_dataset = lambda: representative_dataset(X_rep, rep_count)
    if hasattr(converter, "_experimental_default_to_single_batch_in_tensor_list_ops"):
        converter._experimental_default_to_single_batch_in_tensor_list_ops = True

    if enforce_full_int8:
        converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
        converter.inference_input_type = tf.int8
        converter.inference_output_type = tf.int8

    try:
        tfl_blob = converter.convert()
        notes.append("Exported with builtin TFLite ops path")
    except Exception as exc:
        error_msg = f"QAT conversion is non-deployable under strict full-int8 policy: {exc}"
        notes.append(f"Conversion failed: {exc}")
        payload = {
            "window_size": int(window_size),
            "protocol": protocol,
            "model_name": model_name,
            "run_id": run_id,
            "variant": variant or "default",
            "qat_checkpoint": str(qat_ckpt),
            "qat_tflite": None,
            "input_dtype": None,
            "output_dtype": None,
            "input_dtype_normalized": None,
            "output_dtype_normalized": None,
            "accepted_integer_io_dtypes": accepted_io,
            "full_integer_io": False,
            "representative_source": rep_source,
            "representative_samples": int(rep_count),
            "strict_full_int8": bool(strict_full_int8),
            "require_tflm_compatible": bool(require_tflm_compatible),
            "deployable_full_int8": False,
            "tflm_compatible": False,
            "unsupported_ops": [],
            "tflm_ops": [],
            "compat_error": None,
            "has_unidirectional_sequence_lstm": False,
            "has_while_op": False,
            "training_time_sec": training_time_sec,
            "history_json": str(qat_history_path),
            "epochs_ran": int(len(hist.history.get("loss", []))),
            "status": "failed",
            "error": error_msg,
            "notes": notes,
        }
        dump_json(json_path, payload)
        _write_qat_markdown(md_path, payload)
        raise RuntimeError(error_msg) from exc

    tfl_path.write_bytes(tfl_blob)

    gate = inspect_tflite_and_evaluate_deploy_gate(
        tfl_path,
        accepted_integer_io_dtypes=accepted_io,
        strict_full_int8=strict_full_int8,
        require_tflm_compatible=require_tflm_compatible,
    )
    if gate.get("compat_error"):
        notes.append(f"TFLM compatibility inspection failed: {gate['compat_error']}")

    payload = {
        "window_size": int(window_size),
        "protocol": protocol,
        "model_name": model_name,
        "run_id": run_id,
        "variant": variant or "default",
        "qat_checkpoint": str(qat_ckpt),
        "qat_tflite": str(tfl_path),
        "input_dtype": gate["input_dtype"],
        "output_dtype": gate["output_dtype"],
        "input_dtype_normalized": gate["input_dtype_normalized"],
        "output_dtype_normalized": gate["output_dtype_normalized"],
        "accepted_integer_io_dtypes": gate["accepted_integer_io_dtypes"],
        "full_integer_io": gate["full_integer_io"],
        "representative_source": rep_source,
        "representative_samples": int(rep_count),
        "strict_full_int8": bool(strict_full_int8),
        "require_tflm_compatible": bool(require_tflm_compatible),
        "deployable_full_int8": gate["deployable_full_int8"],
        "tflm_compatible": gate["tflm_compatible"],
        "unsupported_ops": gate["unsupported_ops"],
        "tflm_ops": gate["tflm_ops"],
        "compat_error": gate["compat_error"],
        "has_unidirectional_sequence_lstm": gate["has_unidirectional_sequence_lstm"],
        "has_while_op": gate["has_while_op"],
        "training_time_sec": training_time_sec,
        "history_json": str(qat_history_path),
        "epochs_ran": int(len(hist.history.get("loss", []))),
        "status": gate["status"],
        "error": gate["error"],
        "notes": notes,
    }

    dump_json(json_path, payload)
    _write_qat_markdown(md_path, payload)

    if gate["status"] != "ok" and raise_on_strict_failure:
        raise RuntimeError(
            "QAT conversion is non-deployable under strict full-int8 policy: " + str(gate["error"])
        )

    return {
        "report_json": str(json_path),
        "report_md": str(md_path),
        "tflite": str(tfl_path),
        "history_json": str(qat_history_path),
        "training_time_sec": training_time_sec,
        "epochs_ran": int(len(hist.history.get("loss", []))),
        "status": gate["status"],
        "model_name": model_name,
        "run_id": run_id,
        "variant": variant or "default",
    }


def main() -> None:
    parser = build_parser("Run QAT fine-tuning and export")
    parser.add_argument("--variant", type=str, default=None, help="Optional artifact variant suffix")
    parser.add_argument("--model-name", type=str, default="deepconv_lstm")
    parser.add_argument("--checkpoint-path", type=str, default=None)
    parser.add_argument("--run-id", type=str, default=None)
    parser.add_argument(
        "--annotation-policy",
        type=str,
        default=None,
        help="QAT annotation policy: auto/full/conv_dense/conv2d_dense/dense_only/depthwise_conv2d_dense/all_supported",
    )
    args = parser.parse_args()
    cfg = apply_common_overrides(load_yaml(args.config), args)

    ws = int(cfg["window_size_default"])
    for protocol in cfg.get("split_protocols", ["random_stratified"]):
        out = qat_for_protocol(
            cfg,
            ws,
            protocol,
            model_name=args.model_name,
            checkpoint_path=args.checkpoint_path,
            run_id=args.run_id,
            annotation_policy=args.annotation_policy,
            variant=args.variant,
        )
        print(f"QAT done window_size={ws} protocol={protocol}")
        for k, v in out.items():
            print(f"  - {k}: {v}")


if __name__ == "__main__":
    main()
