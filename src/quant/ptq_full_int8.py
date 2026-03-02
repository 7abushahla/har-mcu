"""Post-training full-integer quantization with strict deployability reporting."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import tensorflow as tf

from src.data.build_dataset import build_dataset_for_protocol
from src.data.io import dataset_exists, load_split_arrays
from src.models.serialization import load_checkpoint_model
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
    model_ptq_tflite_path,
    model_slug,
    ptq_tflite_path,
    run_prefix,
    variant_suffix,
)
from src.utils.config import apply_common_overrides, build_parser, ensure_path_dirs, load_yaml
from src.utils.repro import dump_json


def _make_converter(
    model: tf.keras.Model,
    X_rep,
    rep_count: int,
    *,
    enforce_full_int8: bool,
) -> tf.lite.TFLiteConverter:
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.representative_dataset = lambda: representative_dataset(X_rep, rep_count)

    # RNN/LSTM conversion can fail with TensorList lowering when batch is dynamic.
    if hasattr(converter, "_experimental_default_to_single_batch_in_tensor_list_ops"):
        converter._experimental_default_to_single_batch_in_tensor_list_ops = True

    if enforce_full_int8:
        converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
        converter.inference_input_type = tf.int8
        converter.inference_output_type = tf.int8

    return converter


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
        base = f"ptq_export_T{window_size}_P{protocol}{suffix}"
    else:
        base = f"ptq_export_{run_prefix(model_name, window_size, protocol, run_id)}{suffix}"
    reports_path = Path(reports_dir)
    return reports_path / f"{base}.json", reports_path / f"{base}.md"


def _write_ptq_markdown(md_path: Path, metrics: dict[str, Any]) -> None:
    with md_path.open("w", encoding="utf-8") as f:
        f.write(
            f"# PTQ Export (T={metrics['window_size']}, protocol={metrics['protocol']}, "
            f"variant={metrics['variant']})\n\n"
        )
        if metrics.get("checkpoint"):
            f.write(f"- Checkpoint: `{metrics['checkpoint']}`\n")
        if metrics.get("tflite_model"):
            f.write(f"- TFLite: `{metrics['tflite_model']}`\n")
        if metrics.get("ptq_tflite_size_kb") is not None:
            f.write(f"- PTQ size: {float(metrics['ptq_tflite_size_kb']):.2f} KB\n")
        f.write(f"- Status: `{metrics['status']}`\n")
        f.write(f"- Deployable full integer: `{metrics['deployable_full_int8']}`\n")
        f.write(f"- Full integer I/O: `{metrics['full_integer_io']}`\n")
        f.write(f"- TFLM compatible: `{metrics['tflm_compatible']}`\n")
        f.write(f"- Input dtype: `{metrics['input_dtype']}`\n")
        f.write(f"- Output dtype: `{metrics['output_dtype']}`\n")
        f.write(f"- Accepted integer I/O dtypes: `{metrics['accepted_integer_io_dtypes']}`\n")
        f.write(f"- Representative source: `{metrics['representative_source']}`\n")
        f.write(f"- Representative samples: `{metrics['representative_samples']}`\n")
        if metrics.get("error"):
            f.write(f"- Error: `{metrics['error']}`\n")
        if metrics.get("unsupported_ops"):
            f.write(f"- Unsupported ops: `{', '.join(metrics['unsupported_ops'])}`\n")
        if metrics.get("notes"):
            f.write("\n## Notes\n\n")
            for note in metrics["notes"]:
                f.write(f"- {note}\n")


def quantize_ptq_for_protocol(
    cfg: dict[str, Any],
    window_size: int,
    protocol: str,
    *,
    model_name: str = "deepconv_lstm",
    checkpoint_path: str | None = None,
    run_id: str | None = None,
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
    model = load_checkpoint_model(ckpt_path, compile=False)

    ptq_cfg = cfg.get("quant", {}).get("ptq", {})
    rep_count = int(ptq_cfg.get("representative_samples", 256))
    rep_source = str(ptq_cfg.get("representative_source", "train")).strip().lower()
    strict_full_int8 = bool(ptq_cfg.get("strict_full_int8", True))
    require_tflm_compatible = bool(ptq_cfg.get("require_tflm_compatible", True))
    enforce_full_int8 = bool(ptq_cfg.get("enforce_full_int8", True)) or strict_full_int8
    accepted_io = accepted_integer_dtypes(
        ptq_cfg.get("accepted_integer_io_dtypes", ["int8", "uint8"])
    )

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
    if model_slug(model_name) == "deepconv_lstm" and not run_id:
        model_path = ptq_tflite_path(
            cfg["paths"]["models_tflite_dir"],
            window_size,
            protocol,
            variant=variant,
        )
    else:
        model_path = model_ptq_tflite_path(
            cfg["paths"]["models_tflite_dir"],
            model_name=model_name,
            window_size=window_size,
            protocol=protocol,
            run_id=run_id,
            variant=variant,
        )

    notes: list[str] = []

    try:
        X_rep = representative_array(arrays, rep_source)
    except Exception as exc:
        error_msg = f"Invalid representative source for PTQ: {exc}"
        metrics = {
            "window_size": int(window_size),
            "protocol": protocol,
            "model_name": model_name,
            "run_id": run_id,
            "variant": variant or "default",
            "checkpoint": str(ckpt_path),
            "tflite_model": None,
            "fp32_checkpoint_size_kb": float(ckpt_path.stat().st_size / 1024.0),
            "ptq_tflite_size_kb": None,
            "size_reduction_vs_ckpt_percent": None,
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
            "status": "failed",
            "error": error_msg,
            "notes": notes,
        }
        dump_json(json_path, metrics)
        _write_ptq_markdown(md_path, metrics)
        raise RuntimeError(error_msg) from exc

    converter = _make_converter(model, X_rep, rep_count, enforce_full_int8=enforce_full_int8)

    try:
        tflite_blob = converter.convert()
        notes.append("Converted with builtin TFLite ops path")
    except Exception as exc:
        error_msg = f"PTQ conversion is non-deployable under strict full-int8 policy: {exc}"
        notes.append(f"Conversion failed: {exc}")
        metrics = {
            "window_size": int(window_size),
            "protocol": protocol,
            "model_name": model_name,
            "run_id": run_id,
            "variant": variant or "default",
            "checkpoint": str(ckpt_path),
            "tflite_model": None,
            "fp32_checkpoint_size_kb": float(ckpt_path.stat().st_size / 1024.0),
            "ptq_tflite_size_kb": None,
            "size_reduction_vs_ckpt_percent": None,
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
            "status": "failed",
            "error": error_msg,
            "notes": notes,
        }
        dump_json(json_path, metrics)
        _write_ptq_markdown(md_path, metrics)
        raise RuntimeError(error_msg) from exc

    model_path.parent.mkdir(parents=True, exist_ok=True)
    model_path.write_bytes(tflite_blob)

    gate = inspect_tflite_and_evaluate_deploy_gate(
        model_path,
        accepted_integer_io_dtypes=accepted_io,
        strict_full_int8=strict_full_int8,
        require_tflm_compatible=require_tflm_compatible,
    )
    if gate.get("compat_error"):
        notes.append(f"TFLM compatibility inspection failed: {gate['compat_error']}")

    fp32_size_kb = ckpt_path.stat().st_size / 1024.0
    int8_size_kb = model_path.stat().st_size / 1024.0
    metrics = {
        "window_size": int(window_size),
        "protocol": protocol,
        "model_name": model_name,
        "run_id": run_id,
        "variant": variant or "default",
        "checkpoint": str(ckpt_path),
        "tflite_model": str(model_path),
        "fp32_checkpoint_size_kb": float(fp32_size_kb),
        "ptq_tflite_size_kb": float(int8_size_kb),
        "size_reduction_vs_ckpt_percent": float(
            100.0 * (1.0 - int8_size_kb / max(fp32_size_kb, 1e-9))
        ),
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
        "status": gate["status"],
        "error": gate["error"],
        "notes": notes,
    }
    dump_json(json_path, metrics)
    _write_ptq_markdown(md_path, metrics)

    if gate["status"] != "ok" and raise_on_strict_failure:
        raise RuntimeError(
            "PTQ conversion is non-deployable under strict full-int8 policy: " + str(gate["error"])
        )

    return {
        "tflite_model": str(model_path),
        "report_json": str(json_path),
        "report_md": str(md_path),
        "status": gate["status"],
        "model_name": model_name,
        "run_id": run_id,
        "variant": variant or "default",
    }


def main() -> None:
    parser = build_parser("Export full-integer PTQ model")
    parser.add_argument("--variant", type=str, default=None, help="Optional artifact variant suffix")
    parser.add_argument("--model-name", type=str, default="deepconv_lstm")
    parser.add_argument("--checkpoint-path", type=str, default=None)
    parser.add_argument("--run-id", type=str, default=None)
    args = parser.parse_args()
    cfg = apply_common_overrides(load_yaml(args.config), args)

    ws = int(cfg["window_size_default"])
    for protocol in cfg.get("split_protocols", ["random_stratified"]):
        out = quantize_ptq_for_protocol(
            cfg,
            ws,
            protocol,
            model_name=args.model_name,
            checkpoint_path=args.checkpoint_path,
            run_id=args.run_id,
            variant=args.variant,
        )
        print(f"PTQ done window_size={ws} protocol={protocol}")
        for k, v in out.items():
            print(f"  - {k}: {v}")


if __name__ == "__main__":
    main()
