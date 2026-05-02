"""Copy norm_stats JSON to the experiment `processed_dir` root.

M3 Slurm / arch_seq runs write ``norm_stats_T{w}_P{protocol}.json`` **inside** each
bundle directory (e.g. ``arch_seq/<variant>/e11/finetune_arduino/``), not at
``paths.processed_dir`` from the YAML.  Tools that resolve
``norm_stats_path(processed_dir, window, protocol)`` expect the file at the
**root** of ``processed_dir`` — this script copies an existing bundle file there
**without** rebuilding datasets.

By default, searches under ``--experiment-root`` for
``**/finetune_arduino/norm_stats_*.json`` (first match: Arduino fine-tune stats).
Use ``--glob`` to pick another pattern (e.g. ``**/pretrain_wisdm/norm_stats_*.json``).

Example::

  python scripts/m3_copy_norm_stats_to_experiment_root.py \\
    --experiment-root data/processed/m3/E11_wisdm_pretrain_arduino_finetune_T50
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.utils.artifacts import norm_stats_path  # noqa: E402


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--experiment-root",
        type=Path,
        required=True,
        help="YAML paths.processed_dir (e.g. data/processed/m3/E11_...)",
    )
    p.add_argument(
        "--window",
        type=int,
        default=None,
        help="Window size for dest path (default: inferred from source filename)",
    )
    p.add_argument(
        "--protocol",
        default=None,
        help="Protocol for dest path (default: inferred from source filename)",
    )
    p.add_argument(
        "--glob",
        dest="glob_pat",
        default="**/finetune_arduino/norm_stats_*.json",
        help="Glob under experiment-root to find source JSON (default: finetune_arduino)",
    )
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    exp_root = args.experiment_root.resolve()
    matches = sorted(exp_root.glob(args.glob_pat))
    if not matches:
        raise SystemExit(
            f"No file matched {args.glob_pat!r} under {exp_root}\n"
            "Run dataset build for this experiment first, or pass --glob to an existing norm_stats path."
        )
    src = matches[0]
    if len(matches) > 1:
        print(f"Note: {len(matches)} matches; using first: {src.relative_to(exp_root)}", file=sys.stderr)

    # Parse T{w}_P{protocol} from filename norm_stats_T50_Prandom_stratified.json
    stem = src.stem  # norm_stats_T50_Prandom_stratified
    if not stem.startswith("norm_stats_"):
        raise SystemExit(f"Unexpected norm stats filename: {src.name}")
    rest = stem[len("norm_stats_") :]
    if "_P" not in rest:
        raise SystemExit(f"Cannot parse window/protocol from: {src.name}")
    w_str, p_str = rest.split("_P", 1)
    if not w_str.startswith("T") or not w_str[1:].isdigit():
        raise SystemExit(f"Cannot parse window from: {src.name}")
    window = int(w_str[1:])
    protocol = p_str.replace("_", "-") if "-" not in p_str else p_str  # random_stratified stays

    window = args.window if args.window is not None else window
    protocol = args.protocol if args.protocol is not None else protocol

    dest = norm_stats_path(exp_root, window, protocol)
    print(f"source: {src}")
    print(f"dest:   {dest}")
    if args.dry_run:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    print(f"Copied -> {dest}")


if __name__ == "__main__":
    main()
