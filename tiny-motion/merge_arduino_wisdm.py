#!/usr/bin/env python3
"""
Merge per-class WISDM-style CSVs (from json_to_wisdm_csv.py) into a single
file with the same layout as WISDM_ar_v1.1_raw.csv:

  user,activity,timestamp,x-axis,y-axis,z-axis

WISDM reference
----------------
- https://www.cis.fordham.edu/wisdm/dataset.php
- Each row: one accelerometer sample; public release says 20 Hz (50 ms) steps.
- *user* in WISDM is an integer 1..36. Your exports use *layth* / *hamza*;
  use --numeric-users to write 37 and 38 if you want integer IDs.
- WISDM docs describe *acceleration* in a phone-specific scale where a value
  of 10 ≈ 1g. Arduino JSON values are the Tiny Motion / board pipeline units
  (small magnitudes). This script copies axes as-is; use --acc-scale to match
  a unit convention you document (e.g. trial scaling toward WISDM range).

Why rebase timestamps?
----------------------
Per-class files each start at the same default start-timestamp, so merging
without rebasing would duplicate timestamp values. This script walks all
input rows in a fixed order and assigns monotonically increasing timestamps
in 50 ms (50_000_000 ns) steps, matching WISDM’s nominal row spacing.

Usage
-----
    python3 merge_arduino_wisdm.py -o Arduino_layth_hamza_wisdm_raw.csv

    python3 merge_arduino_wisdm.py \\
        --layth-dir layth_captured/csv_per_class/wisdm \\
        --hamza-dir hamza_captured/csv_per_class/wisdm \\
        -o Arduino_layth_hamza_wisdm_raw.csv

    python3 merge_arduino_wisdm.py --numeric-users -o out.csv
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

STEP_NS = 50_000_000  # 20 Hz spacing, same as json_to_wisdm_csv default step at 0.05 s
START_NS = 4_991_922_345_000  # same default as json_to_wisdm_csv.py

# Fixed read order for reproducibility (all six WISDM activity names)
ACTIVITY_FILES = [
    "walking",
    "jogging",
    "upstairs",
    "downstairs",
    "sitting",
    "standing",
]


def collect_inputs(layth: Path, hamza: Path, wisdm_suffix: str) -> list[Path]:
    out: list[Path] = []
    for name in ACTIVITY_FILES:
        for d, u in ((layth, "layth"), (hamza, "hamza")):
            p = d / f"{u}_{name}{wisdm_suffix}.csv"
            if p.is_file():
                out.append(p)
            else:
                print(f"Warning: missing {p}", flush=True)
    return out


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--layth-dir",
        type=Path,
        default=Path("layth_captured/csv_per_class/wisdm"),
        help="Directory with layth_*{wisdm-suffix}.csv",
    )
    p.add_argument(
        "--hamza-dir",
        type=Path,
        default=Path("hamza_captured/csv_per_class/wisdm"),
        help="Directory with hamza_*{wisdm-suffix}.csv",
    )
    p.add_argument(
        "--wisdm-suffix",
        type=str,
        default="_wisdm_raw",
        help="Input filename suffix (e.g. _wisdm_mps2 for g/4→m/s² per-class exports)",
    )
    p.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("Arduino_layth_hamza_wisdm_raw.csv"),
        help="Output merged CSV path",
    )
    p.add_argument(
        "--start-timestamp",
        type=int,
        default=START_NS,
        help="First output timestamp (nanoseconds)",
    )
    p.add_argument(
        "--step-ns",
        type=int,
        default=STEP_NS,
        help="Nanoseconds between consecutive output rows (default 50 ms)",
    )
    p.add_argument(
        "--acc-scale",
        type=float,
        default=1.0,
        help="Multiply x,y,z (default 1.0; WISDM uses a different scale — document your choice)",
    )
    p.add_argument(
        "--numeric-users",
        action="store_true",
        help="Map layth->37, hamza->38 in user column (WISDM uses integer user IDs)",
    )
    args = p.parse_args()

    inputs = collect_inputs(
        args.layth_dir.resolve(), args.hamza_dir.resolve(), args.wisdm_suffix
    )
    if not inputs:
        print("Error: no input CSVs found", flush=True)
        return 1

    user_map = {"layth": "37", "hamza": "38"} if args.numeric_users else None
    out_path: Path = args.output
    out_path.parent.mkdir(parents=True, exist_ok=True)

    t = int(args.start_timestamp)
    step = int(args.step_ns)
    scale = float(args.acc_scale)
    total = 0

    with out_path.open("w", newline="") as out_f:
        w = csv.DictWriter(
            out_f,
            fieldnames=["user", "activity", "timestamp", "x-axis", "y-axis", "z-axis"],
        )
        w.writeheader()

        for path in inputs:
            with path.open(newline="") as inf:
                r = csv.DictReader(inf)
                for row in r:
                    u = row["user"].strip()
                    if user_map is not None:
                        u = user_map.get(u, u)
                    w.writerow(
                        {
                            "user": u,
                            "activity": row["activity"].strip(),
                            "timestamp": t,
                            "x-axis": float(row["x-axis"]) * scale,
                            "y-axis": float(row["y-axis"]) * scale,
                            "z-axis": float(row["z-axis"]) * scale,
                        }
                    )
                    t += step
                    total += 1

    print(
        f"Wrote {out_path}  ({total} rows, step={step} ns, acc_scale={scale})",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
