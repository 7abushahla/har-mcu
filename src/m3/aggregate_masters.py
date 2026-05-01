"""Merge every per-run `m3_experiment_master.csv` under `reports/m3/` into one table.

Each Slurm `--artifact-suffix` writes masters under a subdirectory (for example
`reports/m3/full_e00/` or `reports/m3/arch_seq/<variant>/e00/`). This tool
collects them into `reports/m3/m3_experiment_master_all.{csv,md}` with a
`results_bundle` column so rows stay traceable to their folder.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.m3.config import M3_MASTER_COLUMNS
from src.utils.markdown_tables import dataframe_to_pipe_markdown


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--reports-dir",
        type=Path,
        default=Path("reports/m3"),
        help="Root M3 reports directory (default: reports/m3 from cwd).",
    )
    p.add_argument(
        "--include-legacy-root",
        action="store_true",
        help="Also read reports/m3/m3_experiment_master.csv at the root of --reports-dir.",
    )
    p.add_argument(
        "--out-prefix",
        default="m3_experiment_master_all",
        help="Basename for merged CSV/MD (default: m3_experiment_master_all).",
    )
    return p.parse_args()


def _bundle_key(csv_path: Path, reports_dir: Path) -> str:
    rel = csv_path.parent.relative_to(reports_dir.resolve())
    return "." if str(rel) == "." else rel.as_posix()


def aggregate_m3_masters(
    reports_dir: Path,
    *,
    include_legacy_root: bool = False,
    out_prefix: str = "m3_experiment_master_all",
) -> dict[str, str]:
    reports_dir = reports_dir.resolve()
    if not reports_dir.is_dir():
        raise FileNotFoundError(f"reports dir not found: {reports_dir}")

    paths = sorted(reports_dir.rglob("m3_experiment_master.csv"))
    legacy = reports_dir / "m3_experiment_master.csv"
    paths = [p.resolve() for p in paths]
    if not include_legacy_root and legacy.resolve() in paths:
        paths = [p for p in paths if p != legacy.resolve()]

    out_csv = reports_dir / f"{out_prefix}.csv"
    out_md = reports_dir / f"{out_prefix}.md"
    paths = [p for p in paths if p != out_csv.resolve()]

    frames: list[pd.DataFrame] = []
    for p in paths:
        df = pd.read_csv(p)
        for col in M3_MASTER_COLUMNS:
            if col not in df.columns:
                df[col] = None
        df = df[M3_MASTER_COLUMNS].copy()
        df.insert(0, "results_bundle", _bundle_key(p, reports_dir))
        frames.append(df)

    if not frames:
        merged = pd.DataFrame(columns=["results_bundle", *M3_MASTER_COLUMNS])
    else:
        merged = pd.concat(frames, ignore_index=True)

    dedup_cols = [
        "results_bundle",
        "experiment_id",
        "model_variant",
        "split_protocol",
        "transfer_mode",
        "seed",
    ]
    merged = merged.drop_duplicates(subset=dedup_cols, keep="last")
    merged = merged.sort_values(
        by=["experiment_id", "model_variant", "results_bundle"],
        kind="stable",
    ).reset_index(drop=True)

    merged.to_csv(out_csv, index=False)
    with out_md.open("w", encoding="utf-8") as f:
        f.write("# M3 experiment master (aggregated)\n\n")
        f.write(
            f"- Rows: `{len(merged)}` (from `{len(paths)}` `m3_experiment_master.csv` files)\n"
        )
        f.write(f"- Reports root: `{reports_dir}`\n\n")
        if not merged.empty:
            f.write(dataframe_to_pipe_markdown(merged))
            f.write("\n")

    return {"csv": str(out_csv), "md": str(out_md), "sources": str(len(paths))}


def main() -> None:
    args = _parse_args()
    out = aggregate_m3_masters(
        args.reports_dir,
        include_legacy_root=args.include_legacy_root,
        out_prefix=args.out_prefix,
    )
    print(out["csv"])
    print(out["md"])
    print(f"sources={out['sources']}")


if __name__ == "__main__":
    main()
