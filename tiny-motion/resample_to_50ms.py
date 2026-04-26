#!/usr/bin/env python3
"""
Properly resample TinyMotion JSON recordings captured at the wrong
0.02 s (50 Hz) delay to the correct 0.05 s (20 Hz), keeping exactly
20 samples per window (matching Hamza's data and the WISDM standard).

Strategy
--------
A simple per-session downsample only yields 8 samples per window —
the wrong shape.  Instead, for every activity label we:

  1. Pool all sessions into one continuous 50 Hz stream.
  2. Resample the stream to 20 Hz via linear interpolation.
  3. Split the stream into non-overlapping 20-sample windows.

Each output window is exactly 20 samples × 0.05 s = 1.0 s, identical
in shape to Hamza's correctly-captured sessions.

The .bak files written by the previous (wrong) script are used as the
source of truth (they still hold the original 50 Hz data).  If no .bak
exists the .json is used directly.

Usage (from this directory):
    python3 resample_to_50ms.py
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

SRC_DT  = 0.02   # original (wrong) sample spacing, seconds
TGT_DT  = 0.05   # correct target sample spacing, seconds
WIN     = 20     # samples per window  (captureSamples)

# Stride for the sliding window applied after resampling.
# At 50 Hz → 20 Hz the pooled stream shrinks by 2.5×.
# A stride of 8 compensates: for ~N original sessions the resampled stream
# has ~N×8 samples, and (N×8 - WIN) / 8 + 1 ≈ N windows — preserving
# the original session count at the correct 20 Hz spacing.
STRIDE  = 8


def pool_resample_rewindow(
    sessions: list[list[dict]],
    src_dt: float,
    tgt_dt: float,
    win: int,
    stride: int,
) -> list[list[dict]]:
    """
    Pool all sessions for one label into a single 50 Hz stream,
    resample to 20 Hz via linear interpolation, then extract overlapping
    win-sample windows with the given stride.

    Stride ≈ 8 at this ratio restores roughly the original session count
    while every window is properly spaced at tgt_dt seconds.
    """
    all_samples = [s for sess in sessions for s in sess]
    n = len(all_samples)
    if n == 0:
        return []

    channels = sorted(all_samples[0].keys(), key=int)

    t_old = np.arange(n, dtype=np.float64) * src_dt
    # Include the endpoint — small fudge avoids floating-point fence-post gaps.
    t_new = np.arange(0, t_old[-1] + tgt_dt * 0.5, tgt_dt, dtype=np.float64)

    # Stack all channels: shape (n, C)
    data_old = np.array(
        [[float(s[ch]) for ch in channels] for s in all_samples],
        dtype=np.float64,
    )

    # Interpolate every channel at once
    data_new = np.zeros((len(t_new), len(channels)), dtype=np.float64)
    for ci in range(len(channels)):
        data_new[:, ci] = np.interp(t_new, t_old, data_old[:, ci])

    # Sliding window with `stride` — discard any partial window at the tail
    new_sessions: list[list[dict]] = []
    for start in range(0, len(t_new) - win + 1, stride):
        window = [
            {ch: float(data_new[start + j, ci]) for ci, ch in enumerate(channels)}
            for j in range(win)
        ]
        new_sessions.append(window)

    return new_sessions


def fix_file(json_path: Path, bak_path: Path) -> None:
    # Prefer the .bak (original 50 Hz data) if it exists
    src = bak_path if bak_path.exists() else json_path
    print(f"\n{'─'*60}")
    print(f"  Source : {src.name}")

    with src.open(encoding="utf-8") as fh:
        data = json.load(fh)

    src_delay = float(data.get("captureSettings.captureDelay", SRC_DT))
    print(f"  captureSettings.captureDelay in source = {src_delay}")

    recordings: list = data["capture.recordings"]
    labels: list    = data.get("capture.labels", [f"label_{i}" for i in range(len(recordings))])

    new_recordings: list = []
    for label, sessions in zip(labels, recordings):
        n_old_sess = len(sessions)
        new_sessions = pool_resample_rewindow(sessions, src_delay, TGT_DT, WIN, STRIDE)
        print(
            f"  [{label}]:  {n_old_sess} sessions × {WIN} samples @ {src_delay} s "
            f"→  {len(new_sessions)} sessions × {WIN} samples @ {TGT_DT} s  (stride={STRIDE})"
        )
        new_recordings.append(new_sessions)

    data["capture.recordings"]          = new_recordings
    data["captureSettings.captureDelay"]  = TGT_DT
    data["captureSettings.captureSamples"] = WIN

    # Back up the original ONLY if not already backed up
    if not bak_path.exists():
        json_path.rename(bak_path)
        print(f"  Original backed up → {bak_path.name}")

    with json_path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, separators=(",", ":"))

    print(f"  Written : {json_path.name}  (captureDelay={TGT_DT}, {WIN} samples/window, stride={STRIDE})")


FILES = [
    "walking.json",
    "jogging.json",
    "upstairs_downstairs.json",
]

if __name__ == "__main__":
    base = Path(__file__).resolve().parent / "layth_captured"
    for fname in FILES:
        fix_file(base / fname, base / (fname + ".bak"))
    print(f"\n{'─'*60}")
    print(f"Done.  All three files: 20 Hz, {WIN} samples/window, stride={STRIDE}, captureDelay={TGT_DT} s.")
