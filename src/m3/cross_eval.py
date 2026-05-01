"""Eval-only cross-domain evaluation for M3 experiments.

Load an existing checkpoint and evaluate it against an already-built processed
dataset split.  No training is performed.  All the data and checkpoints this
needs are already on disk from the original Slurm runs.

Typical usage
-------------
# E09 fine-tuned model evaluated on WISDM test (forgetting / retention check)
python -m src.m3.cross_eval \\
  --experiment-id E09_wisdm_pretrain_arduino_finetune \\
  --model-variant daghero_cnn_2layer_conv2d \\
  --checkpoint checkpoints/m3/E09.../daghero...r0.keras \\
  --processed-dir data/processed/m3/E09.../pretrain_wisdm/ \\
  --eval-domain wisdm \\
  --window-size 100 \\
  --output-dir reports/m3/cross_eval

# E10 model evaluated on WISDM test (uses E00's already-built WISDM split)
python -m src.m3.cross_eval \\
  --experiment-id E10_arduino_from_scratch \\
  --model-variant daghero_cnn_2layer_conv2d \\
  --checkpoint checkpoints/m3/E10.../daghero...r0.keras \\
  --processed-dir data/processed/m3/E00_wisdm_m2_anchor/arch_seq/daghero.../e00/ \\
  --eval-domain wisdm \\
  --window-size 100 \\
  --output-dir reports/m3/cross_eval
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from sklearn.metrics import accuracy_score, f1_score

from src.data.io import load_split_arrays
from src.models.serialization import load_checkpoint_model
from src.utils.constants import DEFAULT_CLASS_ORDER
from src.utils.repro import dump_json


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--experiment-id", required=True,
                   help="Experiment identifier string (e.g. E09_wisdm_pretrain_arduino_finetune)")
    p.add_argument("--model-variant", required=True,
                   help="Model variant string (e.g. daghero_cnn_2layer_conv2d)")
    p.add_argument("--checkpoint", required=True, type=Path,
                   help="Path to the .keras checkpoint to evaluate")
    p.add_argument("--processed-dir", required=True, type=Path,
                   help="Processed dataset dir containing X_test / y_test .npy arrays")
    p.add_argument("--eval-domain", required=True,
                   help="Domain being evaluated (wisdm or arduino) — recorded in output for clarity")
    p.add_argument("--window-size", type=int, default=100,
                   help="Window size used when the processed arrays were built (default: 100)")
    p.add_argument("--protocol", default="random_stratified",
                   help="Split protocol used when the processed arrays were built (default: random_stratified)")
    p.add_argument("--output-dir", type=Path, default=Path("reports/m3/cross_eval"),
                   help="Directory to write the result JSON (default: reports/m3/cross_eval)")
    p.add_argument("--classes", nargs="+", default=DEFAULT_CLASS_ORDER,
                   help="Ordered class label list (default: WISDM DEFAULT_CLASS_ORDER)")
    return p.parse_args()


def run_cross_eval(
    *,
    experiment_id: str,
    model_variant: str,
    checkpoint: Path,
    processed_dir: Path,
    eval_domain: str,
    window_size: int = 100,
    protocol: str = "random_stratified",
    output_dir: Path = Path("reports/m3/cross_eval"),
    classes: list[str] | None = None,
) -> dict:
    if classes is None:
        classes = list(DEFAULT_CLASS_ORDER)

    arrays = load_split_arrays(str(processed_dir), window_size, protocol)
    X_test = arrays["X_test"]
    y_test = arrays["y_test"]

    model = load_checkpoint_model(str(checkpoint), compile=False)
    probs = model.predict(X_test, verbose=0)
    y_pred = probs.argmax(axis=1)

    acc = float(accuracy_score(y_test, y_pred))
    macro_f1 = float(f1_score(y_test, y_pred, average="macro", zero_division=0))

    result = {
        "experiment_id": experiment_id,
        "model_variant": model_variant,
        "eval_domain": eval_domain,
        "window_size": window_size,
        "protocol": protocol,
        "accuracy": acc,
        "macro_f1": macro_f1,
        "n_test_samples": int(len(y_test)),
        "checkpoint": str(checkpoint),
        "processed_dir": str(processed_dir),
        "classes": classes,
    }

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_exp = experiment_id.replace("/", "_")
    safe_mv = model_variant.replace("/", "_")
    out_path = output_dir / f"cross_eval_{safe_exp}_{safe_mv}_{eval_domain}.json"
    dump_json(out_path, result)

    return result


def main() -> None:
    args = _parse_args()
    result = run_cross_eval(
        experiment_id=args.experiment_id,
        model_variant=args.model_variant,
        checkpoint=args.checkpoint,
        processed_dir=args.processed_dir,
        eval_domain=args.eval_domain,
        window_size=args.window_size,
        protocol=args.protocol,
        output_dir=args.output_dir,
        classes=args.classes,
    )
    print(f"experiment_id:  {result['experiment_id']}")
    print(f"model_variant:  {result['model_variant']}")
    print(f"eval_domain:    {result['eval_domain']}")
    print(f"accuracy:       {result['accuracy']:.4f}")
    print(f"macro_f1:       {result['macro_f1']:.4f}")
    print(f"n_test_samples: {result['n_test_samples']}")
    print(f"output:         {result['checkpoint']}")


if __name__ == "__main__":
    main()
