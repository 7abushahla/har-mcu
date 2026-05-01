"""Milestone 3 single-experiment entrypoint.

Run this inside Slurm jobs only. Dry-run mode validates config contracts without
loading datasets or importing TensorFlow-heavy training paths.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
from typing import Any

from src.m3.config import load_m3_config, summarize_m3_config, validate_m3_config


def _append_path_suffix(cfg: dict[str, Any], suffix: str) -> None:
    if not suffix:
        return
    for key in (
        "processed_dir",
        "checkpoints_dir",
        "reports_dir",
        "models_tflite_dir",
        "deploy_common_dir",
    ):
        value = cfg.get("paths", {}).get(key)
        if value:
            cfg["paths"][key] = str(value).rstrip("/") + "/" + suffix.strip("/")


def _apply_smoke_overrides(cfg: dict[str, Any], args: argparse.Namespace) -> None:
    if args.max_windows_per_class is not None:
        cfg.setdefault("smoke", {})["max_windows_per_class"] = int(args.max_windows_per_class)
    if args.artifact_suffix:
        _append_path_suffix(cfg, args.artifact_suffix)
    if args.smoke:
        cfg.setdefault("smoke", {})["enabled"] = True
        cfg.setdefault("train", {})["epochs"] = int(cfg.get("smoke", {}).get("quick_epochs", 1))
        cfg.setdefault("quant", {}).setdefault("qat", {})["epochs"] = 1
        cfg.setdefault("quant", {}).setdefault("ptq", {})["representative_samples"] = int(
            args.representative_samples
        )
        cfg.setdefault("quant", {}).setdefault("qat", {})["representative_samples"] = int(
            args.representative_samples
        )
        timing = cfg.setdefault("eval", {}).setdefault("tflite_timing", {})
        timing["warmup_samples"] = int(args.timing_warmup_samples)
        timing["timed_samples"] = int(args.timing_timed_samples)
    if args.disable_qat:
        cfg.setdefault("quant", {}).setdefault("qat", {})["enabled"] = False


def _print_summary(summary: dict[str, Any]) -> None:
    for key, value in summary.items():
        if isinstance(value, list):
            value = ",".join(str(v) for v in value)
        print(f"{key}: {value}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run or validate one M3 experiment")
    parser.add_argument("--config", required=True, help="Path to configs/m3/E*.yaml")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate config only; do not load data, train, evaluate, or quantize",
    )
    parser.add_argument("--smoke", action="store_true", help="Use tiny smoke settings")
    parser.add_argument("--max-windows-per-class", type=int, default=None)
    parser.add_argument("--artifact-suffix", default=None)
    parser.add_argument("--disable-qat", action="store_true")
    parser.add_argument("--representative-samples", type=int, default=16)
    parser.add_argument("--timing-warmup-samples", type=int, default=2)
    parser.add_argument("--timing-timed-samples", type=int, default=8)
    args = parser.parse_args()

    cfg = load_m3_config(args.config)
    _apply_smoke_overrides(cfg, args)
    errors = validate_m3_config(cfg)
    summary = asdict(summarize_m3_config(cfg))

    if errors:
        print("status: invalid")
        _print_summary(summary)
        print("errors:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(2)

    print("status: valid")
    _print_summary(summary)

    if args.dry_run:
        return

    if not bool(summary.get("enabled", True)) or bool(summary.get("tooling_only", False)):
        print("status: skipped")
        print("reason: config is disabled/tooling-only")
        return

    if "user_holdout" in summary.get("split_protocols", []) and not bool(
        cfg.get("m3", {}).get("allow_user_holdout_run", False)
    ):
        print("status: skipped")
        print("reason: user_holdout execution is disabled by project policy")
        return

    # Single-domain modes reuse the existing FP32/PTQ/QAT runner.
    if (
        summary["transfer_mode"] == "source_only"
        and summary["data_source"] == "wisdm"
    ) or (
        summary["transfer_mode"] == "arduino_from_scratch"
        and summary["data_source"] == "arduino"
    ):
        from src.run_paper_experiment import run_paper_experiment

        out = run_paper_experiment(cfg)
        print(f"rows: {len(out['rows'])}")
        print(f"master_csv: {out['master_exports']['csv']}")
        print(f"master_md: {out['master_exports']['md']}")
        if out.get("m3_master_exports"):
            print(f"m3_master_csv: {out['m3_master_exports']['csv']}")
            print(f"m3_master_md: {out['m3_master_exports']['md']}")
        return

    if summary["transfer_mode"] in {"zero_shot", "finetune"}:
        from src.m3.transfer import run_m3_transfer_experiment

        out = run_m3_transfer_experiment(cfg)
        print(f"rows: {len(out['rows'])}")
        print(f"master_csv: {out['master_exports']['csv']}")
        print(f"master_md: {out['master_exports']['md']}")
        print(f"m3_master_csv: {out['m3_master_exports']['csv']}")
        print(f"m3_master_md: {out['m3_master_exports']['md']}")
        return

    raise NotImplementedError(f"Unsupported M3 execution path: {summary}")


if __name__ == "__main__":
    main()
