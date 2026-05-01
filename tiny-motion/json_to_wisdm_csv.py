#!/usr/bin/env python3
"""
Convert TinyML-style project JSON into a WISDM-like raw CSV:

  user,activity,timestamp,x-axis,y-axis,z-axis

Uses accelerometer only (JSON keys "0","1","2"). Gyroscope is ignored.

Timestamps are synthetic, spaced by captureSettings.captureDelay (seconds),
defaulting to 0.05 s (50 ms), matching the ~50 ms step seen in WISDM_ar_v1.1_raw.csv.

Activity text is derived from each capture label: if the label starts with
"{user}_", the remainder is used (e.g. layth + layth_sitting -> Sitting).
Otherwise the full label is turned into Title Case with spaces for underscores.

Default output is one merged CSV (all classes). Use --per-class for separate files.

Accelerometer axes are copied from the JSON unchanged by default (no unit conversion).

Some firmware (e.g. tf4micro-motion-kit ``data_provider.cpp``) stores ``readAcceleration``
output in **g** but **divided by 4** (±4 g range → values roughly in [-1, 1]). Use
``--acc-pre-multiply 4`` to undo that before ``--acc-scale``. Approximate **m/s²**
like WISDM: ``--acc-pre-multiply 4 --acc-scale 9.80665`` (i.e. stored × 4 × g_Earth).

Usage
-----

Default: one merged file ``<json_stem>_wisdm_raw.csv`` beside the JSON::

    python3 json_to_wisdm_csv.py
    python3 json_to_wisdm_csv.py TinyMLProject.json

Explicit input path and merged output path::

    python3 json_to_wisdm_csv.py /path/to/TinyMLProject.json -o /path/to/out.csv

Another participant name in the ``user`` column (still used to strip ``user_``
prefix from labels when deriving ``activity``)::

    python3 json_to_wisdm_csv.py TinyMLProject.json --user alice

One WISDM-style CSV per capture label (filenames like ``layth_sitting_wisdm_raw.csv``)::

    python3 json_to_wisdm_csv.py TinyMLProject.json --per-class
    python3 json_to_wisdm_csv.py TinyMLProject.json --per-class --out-dir /path/to/csvs

Optional scaling (default: raw JSON, no change)::

    python3 json_to_wisdm_csv.py TinyMLProject.json --acc-scale 9.80665

tf4micro-motion-kit style (stored = g/4) → approximate WISDM m/s²::

    python3 json_to_wisdm_csv.py TinyMLProject.json --acc-pre-multiply 4 --acc-scale 9.80665

Custom first timestamp (nanoseconds) and help::

    python3 json_to_wisdm_csv.py TinyMLProject.json --start-timestamp 5000000000000
    python3 json_to_wisdm_csv.py -h

Arguments
---------

``json_path`` (optional positional)
    Path to the project ``.json``. Default: ``TinyMLProject.json``.

``--user`` (string, default ``layth``)
    Value written in the ``user`` column. If a label is ``layth_sitting`` and
    ``--user layth``, ``activity`` becomes ``Sitting``.

``-o`` / ``--output`` (path, merged mode only)
    Output CSV path. Default: ``<directory>/<json_stem>_wisdm_raw.csv`` (directory
    is from ``--out-dir`` or the JSON's folder).

``--per-class``
    If set, write one CSV per label under ``--out-dir`` (or next to the JSON),
    each restarting at ``--start-timestamp``. If omitted, one continuous merged
    file with timestamps increasing across all labels.

``--out-dir`` (path)
    Base directory for outputs. Default: same directory as ``json_path``.
    Used for default merged output name, for ``-o`` parent creation, and for
    ``--per-class`` files.

``--start-timestamp`` (integer, default ``4991922345000``)
    First row's ``timestamp`` in nanoseconds; each sample adds one step derived
    from ``captureSettings.captureDelay`` in the JSON (e.g. ``0.05`` s → 50_000_000 ns).

``--acc-pre-multiply`` (float, default ``1.0``)
    Multiply each axis **before** ``--acc-scale``. Use ``4`` if JSON values are
    ``g/4`` from firmware (undo the divide-by-4).

``--acc-scale`` (float, default ``1.0``)
    Multiply each axis **after** ``--acc-pre-multiply``. ``1.0`` leaves values
    unchanged aside from pre-multiply. Use ``9.80665`` with pre-multiply ``4``
    to go from stored ``g/4`` to approximate **m/s²**.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


def load_project(json_path: Path) -> dict:
    with json_path.open() as f:
        return json.load(f)


def activity_from_label(label: str, user: str) -> str:
    """WISDM-style activity name (e.g. Sitting, Standing)."""
    label_s = str(label).strip()
    prefix = f"{user.strip()}_"
    if label_s.lower().startswith(prefix.lower()):
        rest = label_s[len(prefix) :]
    else:
        rest = label_s
    rest = rest.replace("_", " ").strip()
    if not rest:
        return label_s
    return rest.title()


def acc_xyz(sample: dict, pre_mult: float, scale: float) -> tuple[float, float, float]:
    x, y, z = float(sample["0"]), float(sample["1"]), float(sample["2"])
    if pre_mult != 1.0:
        x, y, z = x * pre_mult, y * pre_mult, z * pre_mult
    if scale == 1.0:
        return x, y, z
    return (x * scale, y * scale, z * scale)


def write_wisdm_rows(
    writer: csv.DictWriter,
    sessions: list,
    user: str,
    activity: str,
    acc_pre_mult: float,
    acc_scale: float,
    timestamp_ns: int,
    step_ns: int,
) -> tuple[int, int]:
    """
    Write all samples for this label. Returns (end_timestamp_ns, num_rows).
    """
    rows = 0
    t = timestamp_ns
    for session in sessions:
        for sample in session:
            x, y, z = acc_xyz(sample, acc_pre_mult, acc_scale)
            writer.writerow(
                {
                    "user": user,
                    "activity": activity,
                    "timestamp": t,
                    "x-axis": x,
                    "y-axis": y,
                    "z-axis": z,
                }
            )
            t += step_ns
            rows += 1
    return t, rows


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "json_path",
        nargs="?",
        default="TinyMLProject.json",
        type=Path,
        help="Path to project JSON (default: TinyMLProject.json)",
    )
    p.add_argument(
        "--user",
        default="layth",
        help='Value for the "user" column (default: layth)',
    )
    p.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output CSV path for merged mode (default: <json_stem>_wisdm_raw.csv next to JSON)",
    )
    p.add_argument(
        "--per-class",
        action="store_true",
        help="Write one CSV per capture label instead of a single merged file",
    )
    p.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Directory for outputs (default: same folder as JSON); used with --per-class or as base for -o",
    )
    p.add_argument(
        "--start-timestamp",
        type=int,
        default=4_991_922_345_000,
        help="First timestamp in nanoseconds (default matches WISDM scale; monotonic from there)",
    )
    p.add_argument(
        "--acc-pre-multiply",
        type=float,
        default=1.0,
        help="multiply each axis first (default 1.0). Use 4 to undo tf4micro g/4 normalization",
    )
    p.add_argument(
        "--acc-scale",
        type=float,
        default=1.0,
        help="multiply after --acc-pre-multiply (default 1.0: no extra scaling). E.g. 9.80665 for g→m/s²",
    )
    p.add_argument(
        "--wisdm-suffix",
        type=str,
        default="_wisdm_raw",
        help="Filename suffix: per-class {label}{suffix}.csv; merged default {json_stem}{suffix}.csv",
    )
    args = p.parse_args()

    json_path: Path = args.json_path
    if not json_path.is_file():
        print(f"Error: file not found: {json_path}", file=sys.stderr)
        return 1

    data = load_project(json_path)
    labels = data.get("capture.labels")
    recordings = data.get("capture.recordings")
    if not isinstance(labels, list) or not isinstance(recordings, list):
        print("Error: JSON must contain capture.labels and capture.recordings lists.", file=sys.stderr)
        return 1
    if len(labels) != len(recordings):
        print("Error: capture.labels and capture.recordings length mismatch.", file=sys.stderr)
        return 1

    delay_s = float(data.get("captureSettings.captureDelay", 0.05))
    step_ns = int(round(delay_s * 1e9))
    # Confirm ~50 ms when delay is 0.05 (WISDM rows are ~50 ms apart)
    if abs(delay_s - 0.05) < 1e-9:
        print(f"Using sample spacing {delay_s} s -> timestamp step {step_ns} ns (~{step_ns / 1e6:.0f} ms)", flush=True)

    if args.acc_pre_multiply != 1.0:
        print(f"Accelerometer: --acc-pre-multiply {args.acc_pre_multiply} (applied first)", flush=True)
    if args.acc_scale == 1.0 and args.acc_pre_multiply == 1.0:
        print("Accelerometer: raw from JSON (pre-multiply and acc-scale both 1.0)", flush=True)
    elif args.acc_scale != 1.0:
        print(f"Accelerometer: then × --acc-scale {args.acc_scale}", flush=True)

    out_dir = args.out_dir if args.out_dir is not None else json_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    fieldnames = ["user", "activity", "timestamp", "x-axis", "y-axis", "z-axis"]
    user = args.user

    if args.per_class:
        total_rows = 0
        for label, sessions in zip(labels, recordings):
            activity = activity_from_label(label, user)
            safe = str(label).replace(" ", "_")
            out_path = out_dir / f"{safe}{args.wisdm_suffix}.csv"
            t = args.start_timestamp
            with out_path.open("w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=fieldnames)
                w.writeheader()
                t, n = write_wisdm_rows(
                    w, sessions, user, activity, args.acc_pre_multiply, args.acc_scale, t, step_ns
                )
                total_rows += n
            print(f"{out_path}  activity={activity!r}  rows={n}")
        print(f"Total rows: {total_rows}")
        return 0

    out_path = args.output
    if out_path is None:
        out_path = out_dir / f"{json_path.stem}{args.wisdm_suffix}.csv"
    else:
        out_path.parent.mkdir(parents=True, exist_ok=True)

    t = args.start_timestamp
    total_rows = 0
    with out_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for label, sessions in zip(labels, recordings):
            activity = activity_from_label(label, user)
            t, n = write_wisdm_rows(
                w, sessions, user, activity, args.acc_pre_multiply, args.acc_scale, t, step_ns
            )
            total_rows += n

    print(f"{out_path}  rows={total_rows}  user={user!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
