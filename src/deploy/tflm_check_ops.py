"""Check whether TFLite operators are in allowed TFLM resolver set."""

from __future__ import annotations

import argparse
from pathlib import Path

import tensorflow as tf
from src.utils.repro import dump_json

DEFAULT_ALLOWED_OPS = {
    "ADD",
    "CONV_2D",
    "DEQUANTIZE",
    "FULLY_CONNECTED",
    "LOGISTIC",
    "MUL",
    "PACK",
    "QUANTIZE",
    "RESHAPE",
    "SHAPE",
    "SOFTMAX",
    "SPLIT",
    "STRIDED_SLICE",
    "TANH",
    "TRANSPOSE",
    "UNIDIRECTIONAL_SEQUENCE_LSTM",
}


def get_model_ops(model_path: str) -> list[str]:
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    if not hasattr(interpreter, "_get_ops_details"):
        raise RuntimeError("This TensorFlow build does not expose _get_ops_details")

    details = interpreter._get_ops_details()  # pylint: disable=protected-access
    ops = sorted({d.get("op_name", "UNKNOWN") for d in details})
    return ops


def main() -> None:
    parser = argparse.ArgumentParser(description="TFLM op compatibility checker")
    parser.add_argument("--model", required=True, help="Path to tflite model")
    parser.add_argument("--allowed-ops", default=None, help="Comma-separated override list")
    parser.add_argument("--strict", action="store_true", help="Fail on unsupported ops")
    parser.add_argument("--report-json", default="reports/tflm_ops_check.json")
    parser.add_argument("--report-md", default="reports/tflm_ops_check.md")
    args = parser.parse_args()

    allowed = set(DEFAULT_ALLOWED_OPS)
    if args.allowed_ops:
        allowed = {x.strip() for x in args.allowed_ops.split(",") if x.strip()}

    ops = get_model_ops(args.model)
    unsupported = sorted([op for op in ops if op not in allowed])

    payload = {
        "model": args.model,
        "ops": ops,
        "allowed_ops": sorted(allowed),
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
            "Unsupported ops detected for configured TFLM resolver: " + ", ".join(unsupported)
        )

    print(f"compatible: {payload['compatible']}")
    print(f"report_json: {report_json}")
    print(f"report_md: {report_md}")


if __name__ == "__main__":
    main()
