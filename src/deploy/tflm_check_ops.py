"""Check whether TFLite operators are supported by micro_mutable reference set."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from src.deploy.tflm_reference_ops import REFERENCE_OPS_MICRO_MUTABLE_MAIN
from src.utils.repro import dump_json


def get_allowed_ops(
    *,
    allowed_ops_profile: str | None = None,
    allowed_ops_override: Any = None,
) -> tuple[set[str], str]:
    # Legacy parameters intentionally ignored in micro-mutable-only mode.
    _ = allowed_ops_profile
    _ = allowed_ops_override
    return set(REFERENCE_OPS_MICRO_MUTABLE_MAIN), "micro_mutable_main"


def get_model_ops(model_path: str) -> list[str]:
    import tensorflow as tf

    interpreter = tf.lite.Interpreter(
        model_path=model_path,
        experimental_op_resolver_type=tf.lite.experimental.OpResolverType.BUILTIN_WITHOUT_DEFAULT_DELEGATES,
        experimental_delegates=[],
        num_threads=1,
    )
    interpreter.allocate_tensors()

    if not hasattr(interpreter, "_get_ops_details"):
        raise RuntimeError("This TensorFlow build does not expose _get_ops_details")

    details = interpreter._get_ops_details()  # pylint: disable=protected-access
    ops = sorted({d.get("op_name", "UNKNOWN") for d in details})
    return ops


def main() -> None:
    parser = argparse.ArgumentParser(description="TFLM op compatibility checker")
    parser.add_argument("--model", required=True, help="Path to tflite model")
    parser.add_argument(
        "--allowed-ops-profile",
        default="micro_mutable_main",
        help="Deprecated in micro-mutable-only mode; retained for backward CLI compatibility.",
    )
    parser.add_argument(
        "--allowed-ops",
        default=None,
        help="Deprecated in micro-mutable-only mode; retained for backward CLI compatibility.",
    )
    parser.add_argument("--strict", action="store_true", help="Fail on unsupported ops")
    parser.add_argument("--report-json", default="reports/tflm_ops_check.json")
    parser.add_argument("--report-md", default="reports/tflm_ops_check.md")
    args = parser.parse_args()

    override = None
    if args.allowed_ops:
        override = [x.strip() for x in args.allowed_ops.split(",") if x.strip()]
    allowed, profile_used = get_allowed_ops(
        allowed_ops_profile=args.allowed_ops_profile,
        allowed_ops_override=override,
    )

    ops = get_model_ops(args.model)
    unsupported = sorted([op for op in ops if op not in allowed])

    payload = {
        "model": args.model,
        "ops": ops,
        "allowed_ops_profile": profile_used,
        "allowed_ops": sorted(allowed),
        "compatibility_scope": "micro_mutable_main",
        "deprecated_profile_arg": args.allowed_ops_profile,
        "deprecated_allowed_ops_arg": args.allowed_ops,
        "unsupported_ops": unsupported,
        "compatible": len(unsupported) == 0,
    }

    report_json = Path(args.report_json)
    report_md = Path(args.report_md)
    report_json.parent.mkdir(parents=True, exist_ok=True)
    report_md.parent.mkdir(parents=True, exist_ok=True)

    dump_json(report_json, payload)

    with report_md.open("w", encoding="utf-8") as f:
        f.write("# TFLM Operator Compatibility\n\n")
        f.write(f"- Model: `{args.model}`\n")
        f.write(f"- Compatible: `{payload['compatible']}`\n")
        f.write(f"- Unsupported op count: {len(unsupported)}\n\n")
        f.write("## Operators\n\n")
        for op in ops:
            status = "OK" if op in allowed else "MISSING"
            f.write(f"- {op}: {status}\n")

    if args.strict and unsupported:
        raise SystemExit(
            "Unsupported ops detected for micro_mutable_op_resolver.h source: " + ", ".join(unsupported)
        )

    print(f"compatible: {payload['compatible']}")
    print(f"report_json: {report_json}")
    print(f"report_md: {report_md}")


if __name__ == "__main__":
    main()
