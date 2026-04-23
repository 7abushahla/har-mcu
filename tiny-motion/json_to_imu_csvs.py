#!/usr/bin/env python3
"""
Convert TinyML / Edge Impulse-style project JSON into per-class IMU CSV files.

Expects keys like:
  - capture.labels: list of class names
  - capture.recordings: list (parallel to labels) of sessions; each session is
    a list of samples; each sample is {"0":..,"5":..} for acc + gyro.
  - captureSettings.captureSamples, captureThreshold, captureDelay (for filenames)

Output: one CSV per label, same layout as typical motion captures:
  header row, then blocks of N samples separated by blank lines.

Usage
-----

Run from the directory that contains the JSON (default input name)::

    python3 json_to_imu_csvs.py

Read a specific project file; CSVs are written next to the JSON::

    python3 json_to_imu_csvs.py /path/to/TinyMLProject.json

Write all generated CSVs into another folder::

    python3 json_to_imu_csvs.py TinyMLProject.json -o /path/to/output_dir
    python3 json_to_imu_csvs.py TinyMLProject.json --out-dir /path/to/output_dir

Show CLI help (positional + flags)::

    python3 json_to_imu_csvs.py -h

Arguments
---------

``json_path`` (optional positional)
    Path to the project ``.json``. Default: ``TinyMLProject.json`` in the
    current working directory.

``-o`` / ``--out-dir`` (optional)
    Directory for output files. Default: same directory as ``json_path``.

Each output filename is::

    <label>_numSamples_<N>_threshold_<T>_delay_<D>.csv

where ``N``, ``T``, and ``D`` come from ``captureSettings`` inside the JSON.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


def sample_to_row(sample: dict) -> list[float]:
    return [
        float(sample["0"]),
        float(sample["1"]),
        float(sample["2"]),
        float(sample["3"]),
        float(sample["4"]),
        float(sample["5"]),
    ]


def write_class_csv(
    sessions: list,
    out_path: Path,
    header: list[str],
) -> tuple[int, int]:
    """Returns (num_blocks, num_data_rows)."""
    n_blocks = 0
    n_rows = 0
    with out_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        first_block = True
        for session in sessions:
            if not first_block:
                w.writerow([])
            first_block = False
            n_blocks += 1
            for sample in session:
                w.writerow(sample_to_row(sample))
                n_rows += 1
    return n_blocks, n_rows


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
        "-o",
        "--out-dir",
        type=Path,
        default=None,
        help="Directory for CSV files (default: same folder as JSON)",
    )
    args = p.parse_args()

    json_path: Path = args.json_path
    if not json_path.is_file():
        print(f"Error: file not found: {json_path}", file=sys.stderr)
        return 1

    with json_path.open() as f:
        data = json.load(f)

    labels = data.get("capture.labels")
    recordings = data.get("capture.recordings")
    if not isinstance(labels, list) or not isinstance(recordings, list):
        print("Error: JSON must contain capture.labels and capture.recordings lists.", file=sys.stderr)
        return 1
    if len(labels) != len(recordings):
        print("Error: capture.labels and capture.recordings length mismatch.", file=sys.stderr)
        return 1

    labels_full = data.get("bleInterface.dataLabels") or [
        "acc.x",
        "acc.y",
        "acc.z",
        "gyro.x",
        "gyro.y",
        "gyro.z",
    ]
    header = list(labels_full[:6])

    samples = data.get("captureSettings.captureSamples", 20)
    threshold = data.get("captureSettings.captureThreshold", 0)
    delay = data.get("captureSettings.captureDelay", 0.05)

    out_dir = args.out_dir if args.out_dir is not None else json_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    suffix = f"_numSamples_{samples}_threshold_{threshold}_delay_{delay}.csv"

    for label, sessions in zip(labels, recordings):
        safe = str(label).replace(" ", "_")
        out_path = out_dir / f"{safe}{suffix}"
        blocks, rows = write_class_csv(sessions, out_path, header)
        print(f"{out_path}  ({blocks} blocks, {rows} rows)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
