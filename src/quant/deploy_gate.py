"""Shared quantization deploy-gate helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np


def representative_array(arrays: dict[str, np.ndarray], source: str) -> np.ndarray:
    src = str(source).strip().lower()
    if src == "test":
        return arrays["X_test"]
    if src == "train":
        return arrays["X_train"]
    raise ValueError(f"Unsupported representative_source: {source!r} (expected 'train' or 'test')")


def representative_dataset(X: np.ndarray, n_samples: int):
    n = min(len(X), int(n_samples))
    for i in range(n):
        yield [X[i : i + 1].astype(np.float32)]


def normalize_dtype_name(dtype_value: Any) -> str:
    s = str(dtype_value).lower()
    if "uint8" in s:
        return "uint8"
    if "int8" in s:
        return "int8"
    if "float32" in s:
        return "float32"
    return s


def accepted_integer_dtypes(raw: Any) -> list[str]:
    if isinstance(raw, (list, tuple)):
        values = [str(v).strip().lower() for v in raw if str(v).strip()]
        if values:
            return values
    return ["int8", "uint8"]


# ──────────────────────────────────────────────────────────────────────────────
# Delegate-proof op inspection: read ops from the .tflite flatbuffer, not from
# an Interpreter (which can inject runtime "DELEGATE" pseudo-ops).
# ──────────────────────────────────────────────────────────────────────────────
def _tflite_flatbuffer_ops(model_path: str | Path) -> list[str]:
    """Return REAL ops stored inside the .tflite flatbuffer (no DELEGATE possible)."""
    # Local import to keep this module lightweight unless used.
    from tensorflow.lite.python import schema_py_generated as schema_fb

    buf = Path(model_path).read_bytes()
    model = schema_fb.Model.GetRootAsModel(buf, 0)

    # BuiltinOperator enum int -> name
    builtin_map: dict[int, str] = {}
    for k in dir(schema_fb.BuiltinOperator):
        v = getattr(schema_fb.BuiltinOperator, k)
        if isinstance(v, int):
            builtin_map[v] = k

    sub = model.Subgraphs(0)
    ops: list[str] = []
    for i in range(sub.OperatorsLength()):
        op = sub.Operators(i)
        opcode = model.OperatorCodes(op.OpcodeIndex())
        name = builtin_map.get(opcode.BuiltinCode(), str(opcode.BuiltinCode()))
        if name == "CUSTOM":
            name = opcode.CustomCode().decode("utf-8")
        ops.append(name)

    return sorted(set(ops))


def check_tflm_compat(
    model_path: str | Path,
    *,
    allowed_ops_profile: str | None = None,
    allowed_ops_override: Any = None,
) -> tuple[bool, list[str], list[str], str | None, list[str], str]:
    """
    Returns:
      (tflm_compatible, tflm_ops, unsupported_ops, compat_error)

    IMPORTANT:
      - Uses flatbuffer parsing to get ops (delegate-proof).
      - Uses micro_mutable_op_resolver.h reference set as source of truth.
      - allowed_ops_profile/allowed_ops_override are legacy (non-gating).
    """
    try:
        from src.deploy.tflm_reference_ops import REFERENCE_OPS_MICRO_MUTABLE_MAIN

        ops = _tflite_flatbuffer_ops(model_path)
        allowed_ops = set(REFERENCE_OPS_MICRO_MUTABLE_MAIN)
        profile_used = "micro_mutable_main"

        # Sanity: DELEGATE should never appear in flatbuffer ops.
        if "DELEGATE" in ops:
            raise RuntimeError("DELEGATE appeared in flatbuffer ops (should be impossible).")

        unsupported = sorted([op for op in ops if op not in allowed_ops])
        return len(unsupported) == 0, ops, unsupported, None, sorted(allowed_ops), profile_used
    except Exception as exc:
        return False, [], [], str(exc), [], "micro_mutable_main"


def evaluate_deploy_gate_from_details(
    *,
    input_dtype_raw: Any,
    output_dtype_raw: Any,
    accepted_integer_io_dtypes: list[str],
    strict_full_int8: bool,
    require_tflm_compatible: bool,
    tflm_compatible: bool,
    tflm_ops: list[str],
    unsupported_ops: list[str],
    compat_error: str | None,
    allowed_ops_used: list[str] | None = None,
    allowed_ops_profile: str | None = None,
) -> dict[str, Any]:
    from src.deploy.tflm_reference_ops import classify_ops_against_reference

    accepted = accepted_integer_dtypes(accepted_integer_io_dtypes)
    input_norm = normalize_dtype_name(input_dtype_raw)
    output_norm = normalize_dtype_name(output_dtype_raw)

    full_integer_io = (input_norm in accepted) and (output_norm in accepted)
    strict_errors: list[str] = []

    if strict_full_int8 and not full_integer_io:
        strict_errors.append(
            "Model I/O is not in accepted integer dtypes "
            f"(input={input_norm}, output={output_norm}, accepted={accepted})"
        )

    unsupported_micro_mutable = list(unsupported_ops)
    reference_class = classify_ops_against_reference(unsupported_micro_mutable)
    possibly_supported_upstream = reference_class["supported_in_reference"]
    unsupported_in_reference = reference_class["unsupported_in_reference"]
    profile_name = str(allowed_ops_profile or "micro_mutable_main")

    if require_tflm_compatible and not tflm_compatible:
        if compat_error:
            strict_errors.append(f"TFLM compatibility could not be verified: {compat_error}")
        else:
            strict_errors.append(
                "Unsupported ops for micro_mutable_op_resolver.h source: "
                + ", ".join(unsupported_micro_mutable)
            )

    status = "ok" if not strict_errors else "failed"
    error = " | ".join(strict_errors) if strict_errors else None
    deployable_full_int8 = bool(full_integer_io and tflm_compatible)

    return {
        "accepted_integer_io_dtypes": accepted,
        "input_dtype": str(input_dtype_raw),
        "output_dtype": str(output_dtype_raw),
        "input_dtype_normalized": input_norm,
        "output_dtype_normalized": output_norm,
        "compatibility_scope": "micro_mutable_main",
        "full_integer_io": bool(full_integer_io),
        "tflm_compatible": bool(tflm_compatible),
        "unsupported_ops_micro_mutable": unsupported_micro_mutable,
        "unsupported_ops_profile": unsupported_micro_mutable,  # backward-compatible alias
        "unsupported_ops": unsupported_micro_mutable,  # backward-compatible alias
        "tflm_ops": list(tflm_ops),
        "allowed_ops_used": list(allowed_ops_used or []),
        "allowed_ops_profile": profile_name,
        "upstream_reference_tag": reference_class["reference_tag"],
        "possibly_supported_upstream_tflm": possibly_supported_upstream,
        "unsupported_in_reference": unsupported_in_reference,
        "compat_error": compat_error,
        "deployable_full_int8": bool(deployable_full_int8),
        "status": status,
        "error": error,
        "strict_errors": strict_errors,
        "has_unidirectional_sequence_lstm": "UNIDIRECTIONAL_SEQUENCE_LSTM" in set(tflm_ops),
        "has_while_op": "WHILE" in set(tflm_ops),
    }


def inspect_tflite_and_evaluate_deploy_gate(
    model_path: str | Path,
    *,
    accepted_integer_io_dtypes: list[str],
    strict_full_int8: bool,
    require_tflm_compatible: bool,
    allowed_ops_profile: str | None = None,
    allowed_ops_override: Any = None,
) -> dict[str, Any]:
    import tensorflow as tf

    interp = tf.lite.Interpreter(
        model_path=str(model_path),
        experimental_op_resolver_type=tf.lite.experimental.OpResolverType.BUILTIN_WITHOUT_DEFAULT_DELEGATES,
        experimental_delegates=[],
        num_threads=1,
    )
    interp.allocate_tensors()  # ✅ ensure details are populated
    input_dtype_raw = interp.get_input_details()[0]["dtype"]
    output_dtype_raw = interp.get_output_details()[0]["dtype"]

    (
        tflm_compatible,
        tflm_ops,
        unsupported_ops,
        compat_error,
        allowed_ops_used,
        profile_used,
    ) = check_tflm_compat(
        model_path,
        allowed_ops_profile=allowed_ops_profile,
        allowed_ops_override=allowed_ops_override,
    )
    return evaluate_deploy_gate_from_details(
        input_dtype_raw=input_dtype_raw,
        output_dtype_raw=output_dtype_raw,
        accepted_integer_io_dtypes=accepted_integer_io_dtypes,
        strict_full_int8=bool(strict_full_int8),
        require_tflm_compatible=bool(require_tflm_compatible),
        tflm_compatible=tflm_compatible,
        tflm_ops=tflm_ops,
        unsupported_ops=unsupported_ops,
        compat_error=compat_error,
        allowed_ops_used=allowed_ops_used,
        allowed_ops_profile=profile_used,
    )
