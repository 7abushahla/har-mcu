"""Merge every per-run `m3_experiment_master.csv` under `reports/m3/` into one table.

Each Slurm `--artifact-suffix` writes masters under a subdirectory (for example
`reports/m3/full_e00/` or `reports/m3/arch_seq/<variant>/e00/`). This tool
collects them into:

  * `m3_experiment_master_all.{csv,md}` — tall table with a `results_bundle`
    column so rows stay traceable to their folder.

  * `m3_domain_comparison.{csv,md}` — wide pivot where WISDM scores (E00,
    eval_domain=wisdm) are joined onto each Arduino-experiment row for the same
    model_variant, giving `wisdm_fp32_accuracy` and `arduino_fp32_accuracy`
    side by side so domain-gap is immediately visible.

  * `m3_cross_eval_wisdm.{csv,md}` — optional: eval-only WISDM test scores from
    `reports/m3/cross_eval/*.json` (produced by `scripts/run_cross_eval_wisdm.py`).
    These are **not** the same as `wisdm_fp32_accuracy` in `m3_domain_comparison`
    (that column is the E00 anchor); cross-eval rows re-score checkpoints from
    E03–E10 on WISDM splits built for those runs (or E00 WISDM for E10).
"""

from __future__ import annotations

import argparse
import json
import warnings
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

    # Also write domain-split columns to the all-CSV for easy filtering
    domain_cols = [
        "fp32_accuracy", "fp32_macro_f1",
        "ptq_accuracy", "ptq_macro_f1",
        "qat_accuracy", "qat_macro_f1",
    ]
    for col in domain_cols:
        merged[f"wisdm_{col}"] = merged[col].where(merged["eval_domain"] == "wisdm")
        merged[f"arduino_{col}"] = merged[col].where(merged["eval_domain"] == "arduino")
    merged.to_csv(out_csv, index=False)

    return {
        "csv": str(out_csv),
        "md": str(out_md),
        "sources": str(len(paths)),
        "merged": merged,
    }


# ---------------------------------------------------------------------------
# Domain-gap pivot: WISDM baseline joined onto each Arduino experiment row
# ---------------------------------------------------------------------------

_SCORE_COLS = [
    "fp32_accuracy", "fp32_macro_f1",
    "ptq_accuracy", "ptq_macro_f1",
    "qat_accuracy", "qat_macro_f1",
    "model_size_kb", "latency_mean_ms", "latency_p95_ms",
    "deploy_gate_status",
]


def build_domain_comparison(
    merged: pd.DataFrame,
    reports_dir: Path,
    out_prefix: str = "m3_domain_comparison",
) -> dict[str, str]:
    """Wide table: wisdm_<metric> + arduino_<metric> side by side per row.

    Strategy:
    - WISDM baseline = rows where eval_domain=='wisdm' (E00, source_only).
      Keyed by model_variant.
    - Arduino rows = all rows where eval_domain=='arduino'.
    - Join WISDM baseline onto every Arduino row on model_variant so each
      Arduino-experiment row shows the WISDM score side by side.
    - Also include the standalone E00 WISDM rows (arduino cols = NaN).
    """
    wisdm_rows = merged[merged["eval_domain"] == "wisdm"].copy()
    arduino_rows = merged[merged["eval_domain"] == "arduino"].copy()

    # Build WISDM lookup: prefer the E00 / source_only row per model_variant.
    wisdm_anchor = (
        wisdm_rows[wisdm_rows["transfer_mode"] == "source_only"]
        .sort_values("experiment_id")
        .drop_duplicates(subset=["model_variant"], keep="first")
        .set_index("model_variant")
    )
    wisdm_lookup = wisdm_anchor[_SCORE_COLS].rename(
        columns={c: f"wisdm_{c}" for c in _SCORE_COLS}
    )

    identity_cols = [
        "results_bundle", "experiment_id", "model_variant",
        "data_source", "train_domain", "eval_domain",
        "transfer_mode", "unit_mode", "normalization_mode",
        "inference_norm_applied", "window_size_samples",
        "window_duration_seconds", "split_protocol", "seed", "notes",
    ]

    # Arduino section: identity cols + arduino-prefixed scores + joined wisdm scores.
    arduino_out = arduino_rows[
        [c for c in identity_cols if c in arduino_rows.columns]
    ].copy()
    for col in _SCORE_COLS:
        arduino_out[f"arduino_{col}"] = (
            arduino_rows[col].values if col in arduino_rows.columns else None
        )
    arduino_out = arduino_out.join(wisdm_lookup, on="model_variant", how="left")

    # WISDM section: identity cols + wisdm-prefixed scores; arduino cols stay NaN.
    wisdm_out = wisdm_rows[
        [c for c in identity_cols if c in wisdm_rows.columns]
    ].copy()
    for col in _SCORE_COLS:
        wisdm_out[f"wisdm_{col}"] = (
            wisdm_rows[col].values if col in wisdm_rows.columns else None
        )
        wisdm_out[f"arduino_{col}"] = None

    # Align columns so concat sees the same schema on both sides.
    all_cols = list(dict.fromkeys([*arduino_out.columns, *wisdm_out.columns]))
    for col in all_cols:
        if col not in arduino_out.columns:
            arduino_out[col] = None
        if col not in wisdm_out.columns:
            wisdm_out[col] = None

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)
        _combined_raw = pd.concat(
            [arduino_out[all_cols], wisdm_out[all_cols]], ignore_index=True
        )
    combined = _combined_raw.sort_values(
        by=["experiment_id", "model_variant"], kind="stable"
    ).reset_index(drop=True)

    out_csv = reports_dir / f"{out_prefix}.csv"
    out_md = reports_dir / f"{out_prefix}.md"
    combined.to_csv(out_csv, index=False)
    with out_md.open("w", encoding="utf-8") as f:
        f.write("# M3 domain comparison (WISDM vs Arduino)\n\n")
        f.write(
            "Columns prefixed `wisdm_` = WISDM test-set score (from E00 source-only anchor "
            "for the same `model_variant`).  "
            "Columns prefixed `arduino_` = Arduino test-set score from this experiment row.\n\n"
        )
        f.write(f"- Rows: `{len(combined)}`\n\n")
        if not combined.empty:
            f.write(dataframe_to_pipe_markdown(combined))
            f.write("\n")
    return {"csv": str(out_csv), "md": str(out_md)}


def aggregate_cross_eval_wisdm(
    reports_dir: Path,
    *,
    cross_eval_subdir: str = "cross_eval",
    out_prefix: str = "m3_cross_eval_wisdm",
) -> dict[str, str | int]:
    """Merge `reports/m3/cross_eval/cross_eval_*.json` into one CSV/MD (if any)."""
    reports_dir = reports_dir.resolve()
    ce_dir = reports_dir / cross_eval_subdir
    out_csv = reports_dir / f"{out_prefix}.csv"
    out_md = reports_dir / f"{out_prefix}.md"

    if not ce_dir.is_dir():
        return {"csv": str(out_csv), "md": str(out_md), "rows": 0, "skipped": True}

    rows: list[dict] = []
    for jp in sorted(ce_dir.glob("cross_eval_*.json")):
        with jp.open(encoding="utf-8") as f:
            rec = json.load(f)
        rows.append(
            {
                "source_json": jp.name,
                "experiment_id": rec.get("experiment_id"),
                "model_variant": rec.get("model_variant"),
                "eval_domain": rec.get("eval_domain"),
                "window_size": rec.get("window_size"),
                "protocol": rec.get("protocol"),
                "accuracy": rec.get("accuracy"),
                "macro_f1": rec.get("macro_f1"),
                "n_test_samples": rec.get("n_test_samples"),
                "checkpoint": rec.get("checkpoint"),
                "processed_dir": rec.get("processed_dir"),
            }
        )

    if not rows:
        return {"csv": str(out_csv), "md": str(out_md), "rows": 0, "skipped": True}

    df = pd.DataFrame(rows).sort_values(
        by=["experiment_id", "model_variant"], kind="stable"
    ).reset_index(drop=True)
    df.to_csv(out_csv, index=False)
    with out_md.open("w", encoding="utf-8") as f:
        f.write("# M3 cross-eval on WISDM (eval-only, no training)\n\n")
        f.write(
            "Scores from `python scripts/run_cross_eval_wisdm.py` — load a saved checkpoint "
            "and run inference on an existing processed WISDM test split.\n\n"
        )
        f.write(f"- Rows: `{len(df)}`\n\n")
        f.write(dataframe_to_pipe_markdown(df))
        f.write("\n")
    return {"csv": str(out_csv), "md": str(out_md), "rows": len(df), "skipped": False}


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

    cmp = build_domain_comparison(
        out["merged"],
        reports_dir=Path(args.reports_dir).resolve(),
    )
    print(cmp["csv"])
    print(cmp["md"])

    xev = aggregate_cross_eval_wisdm(Path(args.reports_dir).resolve())
    print(xev["csv"])
    print(xev["md"])
    print(f"cross_eval_rows={xev.get('rows', 0)}")


if __name__ == "__main__":
    main()
