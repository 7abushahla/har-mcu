#!/usr/bin/env python3
"""Export train-split z-score stats to Arduino C headers (same format as
``har-mcu/src/deploy/export_norm_header.py`` / ``deploy/common/norm_stats.h``).

Default search locations (under ``--har-mcu``):

  E09 T=100: ``data/processed/m3/E09_wisdm_pretrain_arduino_finetune/norm_stats_T100_Prandom_stratified.json``
             or ``.../full_e09/finetune_arduino/norm_stats_T100_Prandom_stratified.json``
  E11 T=50:  ``data/processed/m3/E11_wisdm_pretrain_arduino_finetune_T50/norm_stats_T50_Prandom_stratified.json``
             or ``.../full_e11/finetune_arduino/norm_stats_T50_Prandom_stratified.json``

If no JSON is found for T=100, falls back to copying ``har-mcu/deploy/common/norm_stats.h``
(E09 Arduino fine-tune train stats per ``reports/m3/final_deployment_summary.md``).

Usage::

  python scripts/export_m3_norm_headers.py
  python scripts/export_m3_norm_headers.py --har-mcu /path/to/har-mcu \
      --t100-json /path/to/norm_stats_T100_....json \
      --t50-json /path/to/norm_stats_T50_....json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _har_mcu_default() -> Path:
    return Path(__file__).resolve().parents[2] / "har-mcu"


def _export_from_json(norm_json: Path, out_h: Path) -> None:
    payload = json.loads(norm_json.read_text(encoding="utf-8"))
    mean = payload["mean"]
    std = payload["std"]
    data = payload.get("data", {})
    unit = data.get("unit_transform", {})
    sampling = data.get("sampling", {})
    window_size = int(payload.get("window_size_samples", payload.get("window_size", 100)))
    sample_rate_hz = int(round(float(sampling.get("target_sample_rate_hz", 20))))
    apply_norm = 1 if bool(payload.get("inference_norm_applied", True)) else 0
    unit_pre_multiply = float(unit.get("pre_multiply", 1.0))
    unit_scale = float(unit.get("scale", 1.0))

    text = "\n".join(
        [
            "/* Generated from norm_stats JSON — train_zscore mean/std on Arduino train split. */",
            "/* Source: " + norm_json.name + " */",
            "#pragma once",
            "",
            f"#define WINDOW_SIZE {window_size}",
            f"#define SAMPLE_RATE_HZ {sample_rate_hz}",
            f"#define APPLY_NORMALIZATION {apply_norm}",
            f"#define UNIT_PRE_MULTIPLY {unit_pre_multiply:.8f}f",
            f"#define UNIT_SCALE {unit_scale:.8f}f",
            "",
            "static constexpr float kNormMean[3] = {" + ", ".join(f"{x:.8f}f" for x in mean) + "};",
            "static constexpr float kNormStd[3] = {" + ", ".join(f"{x:.8f}f" for x in std) + "};",
            f'static constexpr const char* kNormalizationMode = "{payload.get("normalization_mode", "train_zscore")}";',
            f'static constexpr const char* kUnitMode = "{unit.get("unit_mode", "raw_no_conversion")}";',
            "",
        ]
    )
    out_h.parent.mkdir(parents=True, exist_ok=True)
    out_h.write_text(text, encoding="utf-8")


def _first_existing(paths: list[Path]) -> Path | None:
    for p in paths:
        if p.is_file():
            return p
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--har-mcu", type=Path, default=_har_mcu_default())
    ap.add_argument(
        "--out-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "deploy" / "m3_int8_headers",
    )
    ap.add_argument("--t100-json", type=Path, default=None, help="Explicit E09 norm_stats.json")
    ap.add_argument("--t50-json", type=Path, default=None, help="Explicit E11 norm_stats.json")
    args = ap.parse_args()

    har = args.har_mcu.resolve()
    out_dir = args.out_dir.resolve()
    out_t100 = out_dir / "m3_norm_finetune_t100.h"
    out_t50 = out_dir / "m3_norm_finetune_t50.h"

    t100_candidates = []
    if args.t100_json:
        t100_candidates.append(args.t100_json.resolve())
    t100_candidates.extend(
        [
            har / "data/processed/m3/E09_wisdm_pretrain_arduino_finetune/norm_stats_T100_Prandom_stratified.json",
            har
            / "data/processed/m3/E09_wisdm_pretrain_arduino_finetune/full_e09/finetune_arduino/norm_stats_T100_Prandom_stratified.json",
        ]
    )
    t50_candidates = []
    if args.t50_json:
        t50_candidates.append(args.t50_json.resolve())
    t50_candidates.extend(
        [
            har / "data/processed/m3/E11_wisdm_pretrain_arduino_finetune_T50/norm_stats_T50_Prandom_stratified.json",
            har
            / "data/processed/m3/E11_wisdm_pretrain_arduino_finetune_T50/full_e11/finetune_arduino/norm_stats_T50_Prandom_stratified.json",
        ]
    )

    p100 = _first_existing(t100_candidates)
    if p100:
        _export_from_json(p100, out_t100)
        print(f"Wrote {out_t100}  <=  {p100.relative_to(har)}")
    else:
        fallback = har / "deploy/common/norm_stats.h"
        if not fallback.is_file():
            print("error: no T=100 norm JSON and no fallback deploy/common/norm_stats.h", file=sys.stderr)
            return 1
        out_dir.mkdir(parents=True, exist_ok=True)
        text = fallback.read_text(encoding="utf-8")
        banner = (
            "/* m3_norm_finetune_t100.h — copied from har-mcu/deploy/common/norm_stats.h (E09 train z-score).\n"
            " * Regenerate from JSON when available: python scripts/export_m3_norm_headers.py */\n"
        )
        out_t100.write_text(banner + text, encoding="utf-8")
        print(f"Wrote {out_t100}  (fallback copy of {fallback.relative_to(har)})")

    p50 = _first_existing(t50_candidates)
    if p50:
        _export_from_json(p50, out_t50)
        print(f"Wrote {out_t50}  <=  {p50.relative_to(har)}")
    else:
        print(
            "skip T=50: no norm_stats JSON found. After building E11 data in har-mcu, run:\n"
            f"  python scripts/export_m3_norm_headers.py --t50-json <path/to/norm_stats_T50_Prandom_stratified.json>",
            file=sys.stderr,
        )

    readme = out_dir / "README.txt"
    extra = readme.read_text(encoding="utf-8") if readme.is_file() else ""
    # Do not key off "m3_norm_finetune" alone — deploy README may mention those filenames.
    if "Norm headers (z-score on Arduino train split" not in extra:
        readme.parent.mkdir(parents=True, exist_ok=True)
        readme.write_text(
            (extra + "\n" if extra else "")
            + "Norm headers (z-score on Arduino train split, same as offline eval):\n"
            "  m3_norm_finetune_t100.h — E09 finetune, T=100 (include with T=100 model .h)\n"
            "  m3_norm_finetune_t50.h  — E11 finetune, T=50  (include with T=50 model .h)\n"
            "Use kNormMean[3], kNormStd[3], WINDOW_SIZE in your sketch; include only one norm\n"
            "header per firmware build. Regenerate with scripts/export_m3_norm_headers.py\n",
            encoding="utf-8",
        )
        print(f"Updated {readme}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
