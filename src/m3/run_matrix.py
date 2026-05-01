"""Milestone 3 config-matrix entrypoint.

Run this inside Slurm jobs only. Dry-run mode validates configs without data
loading or TensorFlow imports.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict

from src.m3.config import discover_m3_configs, load_m3_config, summarize_m3_config, validate_m3_config


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate or run the M3 config matrix")
    parser.add_argument("--config-dir", default="configs/m3")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    configs = discover_m3_configs(args.config_dir)
    if not configs:
        print(f"status: invalid\nerrors:\n- no E*.yaml configs found in {args.config_dir}")
        raise SystemExit(2)

    any_errors = False
    for path in configs:
        cfg = load_m3_config(path)
        errors = validate_m3_config(cfg)
        summary = asdict(summarize_m3_config(cfg))
        status = "valid" if not errors else "invalid"
        print(
            "|".join(
                [
                    f"config={path}",
                    f"status={status}",
                    f"experiment_id={summary['experiment_id']}",
                    f"model_variant={summary['model_variant']}",
                    f"transfer_mode={summary['transfer_mode']}",
                    f"data_source={summary['data_source']}",
                    f"T={summary['window_size_samples']}",
                    f"target_hz={summary['target_sample_rate_hz']}",
                    f"enabled={summary['enabled']}",
                    f"tooling_only={summary['tooling_only']}",
                ]
            )
        )
        for error in errors:
            print(f"error|{path}|{error}")
        any_errors = any_errors or bool(errors)

    if any_errors:
        raise SystemExit(2)
    if args.dry_run:
        return

    enabled_configs = []
    for path in configs:
        summary = asdict(summarize_m3_config(load_m3_config(path)))
        if summary.get("enabled", True) and not summary.get("tooling_only", False):
            enabled_configs.append(path)
    if len(enabled_configs) != len(configs):
        print("disabled/tooling-only configs are skipped for execution by default")

    raise NotImplementedError(
        "Matrix execution is intentionally gated until the full M3 transfer "
        "runner is wired. Submit individual supported configs for now."
    )


if __name__ == "__main__":
    main()
