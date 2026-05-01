"""Run all missing WISDM cross-domain evaluations locally (no training / no GPU needed).

Covers:
  E03-E07  zero-shot WISDM→Arduino experiments  → eval on source_wisdm/  (T=100)
  E08      T=50 window zero-shot                → eval on source_wisdm/  (T=50)
  E09      pretrain WISDM, finetune Arduino     → eval on pretrain_wisdm/ (T=100)
  E10      Arduino from-scratch                  → eval on E00 WISDM data  (T=100)
  E11      same as E09, T=50                     → eval on pretrain_wisdm/ (T=50)
  E12      same as E10, T=50                     → eval on E08 source_wisdm/ (T=50)

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
OUT  = ROOT / "reports" / "m3" / "cross_eval"


@dataclass
class Job:
    experiment_id: str
    model_variant: str
    checkpoint: Path
    processed_dir: Path
    eval_domain: str
    window_size: int


def _checkpoint(exp_dir: str, variant: str, exp_code: str, window: int) -> Path:
    """Construct the FP32 final checkpoint path under arch_seq."""
    fname = (
        f"{variant}_T{window}_Prandom_stratified_{exp_code}_{variant}_r0.keras"
    )
    return BASE / exp_dir / "arch_seq" / variant / exp_code.lower() / fname


def build_jobs() -> list[Job]:
    jobs: list[Job] = []

    # ------------------------------------------------------------------ #
    # E03-E07: zero-shot WISDM→Arduino (T=100) — eval on source_wisdm
    # ------------------------------------------------------------------ #
    zero_shot_exps = [
        ("E03_arduino_downsample_20hz_T100", "E03"),
        ("E04_wisdm_to_g_arduino_g",         "E04"),
        ("E05_legacy_arduino_to_mps2",       "E05"),
        ("E06_no_norm_matched",              "E06"),
        ("E07_skip_inference_norm_diag",     "E07"),
    ]
    for exp_dir, exp_code in zero_shot_exps:
        for variant in VARIANTS:
            ck = _checkpoint(exp_dir, variant, exp_code, window=100)
            pd = PROC / exp_dir / "arch_seq" / variant / exp_code.lower() / "source_wisdm"
            if not ck.exists():
                print(f"[SKIP-no-ckpt] {exp_code} {variant}")
                continue
            if not pd.exists():
                print(f"[SKIP-no-proc] {exp_code} {variant} source_wisdm")
                continue
            jobs.append(Job(exp_code, variant, ck, pd, "wisdm", 100))

    # ------------------------------------------------------------------ #
    # E08: T=50 window zero-shot — eval on source_wisdm
    # ------------------------------------------------------------------ #
    for variant in VARIANTS:
        ck = _checkpoint("E08_T50_window", variant, "E08", window=50)
        pd = PROC / "E08_T50_window" / "arch_seq" / variant / "e08" / "source_wisdm"
        if not ck.exists():
            print(f"[SKIP-no-ckpt] E08 {variant}")
            continue
        if not pd.exists():
            print(f"[SKIP-no-proc] E08 {variant} source_wisdm")
            continue
        jobs.append(Job("E08", variant, ck, pd, "wisdm", 50))

    # ------------------------------------------------------------------ #
    # E09: finetune — eval final model on pretrain_wisdm (forgetting check)
    # ------------------------------------------------------------------ #
    for variant in VARIANTS:
        ck = _checkpoint("E09_wisdm_pretrain_arduino_finetune", variant, "E09", window=100)
        pd = PROC / "E09_wisdm_pretrain_arduino_finetune" / "arch_seq" / variant / "e09" / "pretrain_wisdm"
        if not ck.exists():
            print(f"[SKIP-no-ckpt] E09 {variant}")
            continue
        if not pd.exists():
            print(f"[SKIP-no-proc] E09 {variant} pretrain_wisdm")
            continue
        jobs.append(Job("E09", variant, ck, pd, "wisdm", 100))

    # ------------------------------------------------------------------ #
    # E10: from-scratch Arduino — eval on E00's WISDM test set
    # ------------------------------------------------------------------ #
    for variant in VARIANTS:
        ck = _checkpoint("E10_arduino_from_scratch", variant, "E10", window=100)
        # Reuse E00's already-built WISDM processed data (same T=100, same WISDM split)
        pd = PROC / "E00_wisdm_m2_anchor" / "arch_seq" / variant / "e00"
        if not ck.exists():
            print(f"[SKIP-no-ckpt] E10 {variant}")
            continue
        if not pd.exists():
            print(f"[SKIP-no-proc] E10 {variant} (E00 wisdm)")
            continue
        jobs.append(Job("E10", variant, ck, pd, "wisdm", 100))

    # ------------------------------------------------------------------ #
    # E11: pretrain WISDM, finetune Arduino T=50 — forgetting check
    # ------------------------------------------------------------------ #
    for variant in VARIANTS:
        ck = _checkpoint("E11_wisdm_pretrain_arduino_finetune_T50", variant, "E11", window=50)
        pd = PROC / "E11_wisdm_pretrain_arduino_finetune_T50" / "arch_seq" / variant / "e11" / "pretrain_wisdm"
        if not ck.exists():
            print(f"[SKIP-no-ckpt] E11 {variant}")
            continue
        if not pd.exists():
            print(f"[SKIP-no-proc] E11 {variant} pretrain_wisdm")
            continue
        jobs.append(Job("E11", variant, ck, pd, "wisdm", 50))

    # ------------------------------------------------------------------ #
    # E12: from-scratch Arduino T=50 — eval on E08's source_wisdm split
    # (E08 is the T=50 WISDM-trained anchor, same window size)
    # ------------------------------------------------------------------ #
    for variant in VARIANTS:
        ck = _checkpoint("E12_arduino_from_scratch_T50", variant, "E12", window=50)
        pd = PROC / "E08_T50_window" / "arch_seq" / variant / "e08" / "source_wisdm"
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
        out_file = OUT / f"cross_eval_{job.experiment_id}_{job.model_variant}_wisdm.json"
        if out_file.exists():
            print(f"[{i:3d}/{len(jobs)}] SKIP (already done): {job.experiment_id} {job.model_variant}")
            continue
        print(f"[{i:3d}/{len(jobs)}] {job.experiment_id}  {job.model_variant} ...", flush=True)
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
        print(f"         acc={result['accuracy']:.4f}  f1={result['macro_f1']:.4f}  n={result['n_test_samples']}")


if __name__ == "__main__":
    main()
