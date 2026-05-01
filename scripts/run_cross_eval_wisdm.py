"""Run M3 eval-only cross-domain checks locally (no training / no GPU needed).

Covers:
  E03-E12  WISDM test re-score (see build_jobs)
  E00      Arduino test re-score (E00 checkpoints on E03's eval_arduino splits)

Usage (from repo root, conda env active):
  python scripts/run_cross_eval_wisdm.py
  python scripts/run_cross_eval_wisdm.py --dry-run   # just print the job list
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.m3.cross_eval import run_cross_eval  # noqa: E402

VARIANTS = [
    "daghero_cnn_2layer_conv2d",
    "deepconv_lstm_conv2d",
    "repmobile_folded_conv2d",
    "tcn_attention_har_teacher_conv2d",
    "tcn_inception_conv2d",
    "xtinyhar_student_conv2d",
    "xtinyhar_student_conv2d_relu",
]

BASE = ROOT / "checkpoints" / "m3"
PROC = ROOT / "data" / "processed" / "m3"
OUT = ROOT / "reports" / "m3" / "cross_eval"

# E03 provides per-architecture Arduino eval tensors (WISDM-train z-score stats).
E03_DIR = "E03_arduino_downsample_20hz_T100"


@dataclass
class Job:
    experiment_id: str
    model_variant: str
    checkpoint: Path
    processed_dir: Path
    eval_domain: str
    window_size: int


def _checkpoint_arch_seq(exp_dir: str, variant: str, exp_code: str, window: int) -> Path:
    fname = f"{variant}_T{window}_Prandom_stratified_{exp_code}_{variant}_r0.keras"
    return BASE / exp_dir / "arch_seq" / variant / exp_code.lower() / fname


def _checkpoint_full_e_deepconv(exp_dir: str, exp_code_upper: str, window: int) -> Path:
    """FP32 deepconv checkpoint under checkpoints/m3/<exp>/full_eXX/."""
    sub = f"full_{exp_code_upper.lower()}"
    fname = (
        f"deepconv_lstm_conv2d_T{window}_Prandom_stratified_{exp_code_upper}_deepconv_lstm_r0.keras"
    )
    return BASE / exp_dir / sub / fname


def _e00_checkpoint(variant: str) -> Path:
    if variant == "deepconv_lstm_conv2d":
        return BASE / "E00_wisdm_m2_anchor" / "full_e00" / (
            "deepconv_lstm_conv2d_T100_Prandom_stratified_E00_deepconv_lstm_r0.keras"
        )
    return _checkpoint_arch_seq("E00_wisdm_m2_anchor", variant, "E00", window=100)


def _e03_eval_arduino_for_variant(variant: str) -> Path:
    if variant == "deepconv_lstm_conv2d":
        return PROC / E03_DIR / "full_e03" / "eval_arduino"
    return PROC / E03_DIR / "arch_seq" / variant / "e03" / "eval_arduino"


def build_jobs() -> list[Job]:
    jobs: list[Job] = []

    # ------------------------------------------------------------------ #
    # E00: WISDM-trained checkpoints → Arduino test (E03 eval_arduino splits)
    # ------------------------------------------------------------------ #
    for variant in VARIANTS:
        ck = _e00_checkpoint(variant)
        pd = _e03_eval_arduino_for_variant(variant)
        if not ck.exists():
            print(f"[SKIP-no-ckpt] E00 {variant} arduino")
            continue
        if not pd.exists():
            print(f"[SKIP-no-proc] E00 {variant} eval_arduino")
            continue
        jobs.append(Job("E00", variant, ck, pd, "arduino", 100))

    # ------------------------------------------------------------------ #
    # E03-E07: zero-shot — arch_seq WISDM (existing) + full_e deepconv WISDM
    # ------------------------------------------------------------------ #
    zero_shot_exps = [
        ("E03_arduino_downsample_20hz_T100", "E03"),
        ("E04_wisdm_to_g_arduino_g", "E04"),
        ("E05_legacy_arduino_to_mps2", "E05"),
        ("E06_no_norm_matched", "E06"),
        ("E07_skip_inference_norm_diag", "E07"),
    ]
    for exp_dir, exp_code in zero_shot_exps:
        for variant in VARIANTS:
            ck = _checkpoint_arch_seq(exp_dir, variant, exp_code, window=100)
            pd = PROC / exp_dir / "arch_seq" / variant / exp_code.lower() / "source_wisdm"
            if variant == "deepconv_lstm_conv2d":
                ck = _checkpoint_full_e_deepconv(exp_dir, exp_code, window=100)
                pd = PROC / exp_dir / f"full_{exp_code.lower()}" / "source_wisdm"
            if not ck.exists():
                print(f"[SKIP-no-ckpt] {exp_code} {variant}")
                continue
            if not pd.exists():
                print(f"[SKIP-no-proc] {exp_code} {variant} source_wisdm")
                continue
            jobs.append(Job(exp_code, variant, ck, pd, "wisdm", 100))

    # ------------------------------------------------------------------ #
    # E08: T=50 zero-shot — arch_seq + full_e deepconv
    # ------------------------------------------------------------------ #
    for variant in VARIANTS:
        ck = _checkpoint_arch_seq("E08_T50_window", variant, "E08", window=50)
        pd = PROC / "E08_T50_window" / "arch_seq" / variant / "e08" / "source_wisdm"
        if variant == "deepconv_lstm_conv2d":
            ck = _checkpoint_full_e_deepconv("E08_T50_window", "E08", window=50)
            pd = PROC / "E08_T50_window" / "full_e08" / "source_wisdm"
        if not ck.exists():
            print(f"[SKIP-no-ckpt] E08 {variant}")
            continue
        if not pd.exists():
            print(f"[SKIP-no-proc] E08 {variant} source_wisdm")
            continue
        jobs.append(Job("E08", variant, ck, pd, "wisdm", 50))

    # ------------------------------------------------------------------ #
    # E09: finetune — arch_seq + full_e09 deepconv → pretrain_wisdm
    # ------------------------------------------------------------------ #
    for variant in VARIANTS:
        ck = _checkpoint_arch_seq("E09_wisdm_pretrain_arduino_finetune", variant, "E09", window=100)
        pd = (
            PROC / "E09_wisdm_pretrain_arduino_finetune" / "arch_seq" / variant / "e09" / "pretrain_wisdm"
        )
        if variant == "deepconv_lstm_conv2d":
            ck = _checkpoint_full_e_deepconv("E09_wisdm_pretrain_arduino_finetune", "E09", window=100)
            pd = PROC / "E09_wisdm_pretrain_arduino_finetune" / "full_e09" / "pretrain_wisdm"
        if not ck.exists():
            print(f"[SKIP-no-ckpt] E09 {variant}")
            continue
        if not pd.exists():
            print(f"[SKIP-no-proc] E09 {variant} pretrain_wisdm")
            continue
        jobs.append(Job("E09", variant, ck, pd, "wisdm", 100))

    # ------------------------------------------------------------------ #
    # E10: from-scratch — arch_seq + full_e10 deepconv → E00 full_e00 WISDM
    # ------------------------------------------------------------------ #
    for variant in VARIANTS:
        ck = _checkpoint_arch_seq("E10_arduino_from_scratch", variant, "E10", window=100)
        pd = PROC / "E00_wisdm_m2_anchor" / "arch_seq" / variant / "e00"
        if variant == "deepconv_lstm_conv2d":
            ck = _checkpoint_full_e_deepconv("E10_arduino_from_scratch", "E10", window=100)
            pd = PROC / "E00_wisdm_m2_anchor" / "full_e00"
        if not ck.exists():
            print(f"[SKIP-no-ckpt] E10 {variant}")
            continue
        if not pd.exists():
            print(f"[SKIP-no-proc] E10 {variant} (E00 wisdm)")
            continue
        jobs.append(Job("E10", variant, ck, pd, "wisdm", 100))

    # ------------------------------------------------------------------ #
    # E11: T=50 finetune (all arch_seq, including deepconv — already on disk)
    # ------------------------------------------------------------------ #
    for variant in VARIANTS:
        ck = _checkpoint_arch_seq("E11_wisdm_pretrain_arduino_finetune_T50", variant, "E11", window=50)
        pd = (
            PROC / "E11_wisdm_pretrain_arduino_finetune_T50" / "arch_seq" / variant / "e11" / "pretrain_wisdm"
        )
        if not ck.exists():
            print(f"[SKIP-no-ckpt] E11 {variant}")
            continue
        if not pd.exists():
            print(f"[SKIP-no-proc] E11 {variant} pretrain_wisdm")
            continue
        jobs.append(Job("E11", variant, ck, pd, "wisdm", 50))

    # ------------------------------------------------------------------ #
    # E12: T=50 from-scratch — arch_seq + full_e08 deepconv for WISDM tensors
    # ------------------------------------------------------------------ #
    for variant in VARIANTS:
        ck = _checkpoint_arch_seq("E12_arduino_from_scratch_T50", variant, "E12", window=50)
        pd = PROC / "E08_T50_window" / "arch_seq" / variant / "e08" / "source_wisdm"
        if variant == "deepconv_lstm_conv2d":
            ck = _checkpoint_arch_seq("E12_arduino_from_scratch_T50", variant, "E12", window=50)
            pd = PROC / "E08_T50_window" / "full_e08" / "source_wisdm"
        if not ck.exists():
            print(f"[SKIP-no-ckpt] E12 {variant}")
            continue
        if not pd.exists():
            print(f"[SKIP-no-proc] E12 {variant} (E08 T50 wisdm)")
            continue
        jobs.append(Job("E12", variant, ck, pd, "wisdm", 50))

    return jobs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Print jobs without running them")
    args = parser.parse_args()

    jobs = build_jobs()
    print(f"\n{'DRY-RUN: ' if args.dry_run else ''}Running {len(jobs)} cross-eval jobs\n")

    for i, job in enumerate(jobs, 1):
        safe_exp = job.experiment_id.replace("/", "_")
        safe_mv = job.model_variant.replace("/", "_")
        out_file = OUT / f"cross_eval_{safe_exp}_{safe_mv}_{job.eval_domain}.json"
        if out_file.exists():
            print(f"[{i:3d}/{len(jobs)}] SKIP (already done): {job.experiment_id} {job.model_variant} {job.eval_domain}")
            continue
        print(f"[{i:3d}/{len(jobs)}] {job.experiment_id}  {job.model_variant}  {job.eval_domain} ...", flush=True)
        if args.dry_run:
            print(f"         ck: {job.checkpoint}")
            print(f"         pd: {job.processed_dir}")
            continue
        result = run_cross_eval(
            experiment_id=job.experiment_id,
            model_variant=job.model_variant,
            checkpoint=job.checkpoint,
            processed_dir=job.processed_dir,
            eval_domain=job.eval_domain,
            window_size=job.window_size,
            output_dir=OUT,
        )
        print(
            f"         acc={result['accuracy']:.4f}  f1={result['macro_f1']:.4f}  "
            f"n={result['n_test_samples']}"
        )


if __name__ == "__main__":
    main()
