"""Axis-level EDA for M3 WISDM-vs-Arduino accelerometer data."""

from __future__ import annotations

import argparse
import csv
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from src.data.load_har import load_har_dataframe
from src.data.preprocess_zhou2025 import preprocess_zhou2025
from src.data.resample import maybe_downsample_dataframe
from src.data.units import apply_unit_transform
from src.data.windowing import generate_windows
from src.m3.config import load_m3_config
from src.utils.constants import AXIS_COLUMNS, DEFAULT_CLASS_ORDER


def _prepare_domain(cfg: dict[str, Any], domain: str) -> tuple[pd.DataFrame, dict[str, Any]]:
    raw_df, raw_meta = load_har_dataframe(cfg, domain=domain)
    clean_df, clean_meta = preprocess_zhou2025(raw_df, cfg)
    unit_df, unit_meta = apply_unit_transform(clean_df, cfg, domain=domain)
    sampled_df, sample_meta = maybe_downsample_dataframe(unit_df, cfg)
    return sampled_df, {
        "raw": raw_meta,
        "preprocess": clean_meta,
        "unit": unit_meta,
        "sampling": sample_meta,
    }


def _quantile(series: pd.Series, q: float) -> float:
    return float(series.quantile(q))


def _sample_summary(df: pd.DataFrame, domain: str) -> list[dict[str, Any]]:
    work = df.copy()
    axis = work[AXIS_COLUMNS].astype(float)
    work["vector_norm"] = np.linalg.norm(axis.to_numpy(dtype=np.float32), axis=1)
    rows: list[dict[str, Any]] = []
    for activity, group in work.groupby("activity", sort=True):
        row: dict[str, Any] = {
            "domain": domain,
            "activity": activity,
            "samples": int(len(group)),
            "users": int(group["user"].nunique()),
            "vector_norm_mean": float(group["vector_norm"].mean()),
            "vector_norm_std": float(group["vector_norm"].std(ddof=0)),
            "vector_norm_p05": _quantile(group["vector_norm"], 0.05),
            "vector_norm_p50": _quantile(group["vector_norm"], 0.50),
            "vector_norm_p95": _quantile(group["vector_norm"], 0.95),
        }
        for col in AXIS_COLUMNS:
            row[f"{col}_mean"] = float(group[col].mean())
            row[f"{col}_std"] = float(group[col].std(ddof=0))
            row[f"{col}_p05"] = _quantile(group[col], 0.05)
            row[f"{col}_p50"] = _quantile(group[col], 0.50)
            row[f"{col}_p95"] = _quantile(group[col], 0.95)
        rows.append(row)
    return rows


def _window_summary(
    df: pd.DataFrame,
    cfg: dict[str, Any],
    domain: str,
    window_size: int,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    class_order = cfg.get("classes") or DEFAULT_CLASS_ORDER
    class_to_idx = {name: i for i, name in enumerate(class_order)}
    X, y, _users, _stats = generate_windows(
        df,
        window_size=window_size,
        overlap=float(cfg["overlap"]),
        label_policy=str(cfg.get("label_policy", "drop_cross_boundary")),
        class_to_idx=class_to_idx,
        max_windows_per_class=None,
    )
    idx_to_class = {i: name for name, i in class_to_idx.items()}
    rows: list[dict[str, Any]] = []
    dominant_rows: list[dict[str, Any]] = []
    axis_names = ["x", "y", "z"]

    for label_idx in sorted(np.unique(y).tolist()):
        activity = idx_to_class[int(label_idx)]
        windows = X[y == label_idx].astype(np.float32)
        mean_vec = windows.mean(axis=1)
        centered = windows - mean_vec[:, None, :]
        dynamic_rms = np.sqrt(np.mean(np.sum(centered * centered, axis=2), axis=1))
        sample_norm = np.linalg.norm(windows, axis=2)
        mean_norm = np.linalg.norm(mean_vec, axis=1)

        row: dict[str, Any] = {
            "domain": domain,
            "activity": activity,
            "windows": int(len(windows)),
            "mean_vector_norm_mean": float(mean_norm.mean()),
            "mean_vector_norm_std": float(mean_norm.std(ddof=0)),
            "sample_norm_mean": float(sample_norm.mean()),
            "sample_norm_std": float(sample_norm.std(ddof=0)),
            "dynamic_rms_mean": float(dynamic_rms.mean()),
            "dynamic_rms_std": float(dynamic_rms.std(ddof=0)),
        }
        for i, axis_name in enumerate(axis_names):
            row[f"window_mean_{axis_name}_mean"] = float(mean_vec[:, i].mean())
            row[f"window_mean_{axis_name}_std"] = float(mean_vec[:, i].std(ddof=0))
        rows.append(row)

        dominant = np.argmax(np.abs(mean_vec), axis=1)
        signs = np.where(mean_vec[np.arange(len(mean_vec)), dominant] >= 0.0, "positive", "negative")
        counts = Counter((axis_names[int(axis_idx)], str(sign)) for axis_idx, sign in zip(dominant, signs))
        for axis_name in axis_names:
            for sign in ("positive", "negative"):
                count = counts.get((axis_name, sign), 0)
                dominant_rows.append(
                    {
                        "domain": domain,
                        "activity": activity,
                        "dominant_axis": axis_name,
                        "sign": sign,
                        "windows": int(count),
                        "fraction": float(count / len(windows)) if len(windows) else 0.0,
                    }
                )
    return rows, dominant_rows


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _write_markdown(
    path: Path,
    *,
    config_path: Path,
    window_size: int,
    sample_rows: list[dict[str, Any]],
    window_rows: list[dict[str, Any]],
    meta: dict[str, dict[str, Any]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    by_domain_activity = {(r["domain"], r["activity"]): r for r in window_rows}
    with path.open("w", encoding="utf-8") as f:
        f.write("# M3 Axis EDA\n\n")
        f.write(f"- Config: `{config_path}`\n")
        f.write(f"- Window size: `{window_size}` samples\n")
        for domain, domain_meta in meta.items():
            unit = domain_meta["unit"]
            sampling = domain_meta["sampling"]
            raw = domain_meta["raw"]
            f.write(
                f"- `{domain}`: rows `{raw['rows']}`, users `{raw['user_count']}`, "
                f"unit mode `{unit['unit_mode']}`, total scale `{unit['total_scale']}`, "
                f"downsample `{sampling['downsample']}`\n"
            )
        f.write("\n## Window Energy Summary\n\n")
        f.write("| Activity | WISDM dynamic RMS | Arduino dynamic RMS | Arduino-WISDM | WISDM mean-vector norm | Arduino mean-vector norm |\n")
        f.write("| --- | ---: | ---: | ---: | ---: | ---: |\n")
        activities = sorted({r["activity"] for r in sample_rows})
        for activity in activities:
            w = by_domain_activity.get(("wisdm", activity))
            a = by_domain_activity.get(("arduino", activity))
            if not w or not a:
                continue
            delta = float(a["dynamic_rms_mean"]) - float(w["dynamic_rms_mean"])
            f.write(
                f"| {activity} | {float(w['dynamic_rms_mean']):.4f} | {float(a['dynamic_rms_mean']):.4f} | "
                f"{delta:+.4f} | {float(w['mean_vector_norm_mean']):.4f} | {float(a['mean_vector_norm_mean']):.4f} |\n"
            )
        f.write("\nInterpretation notes:\n\n")
        f.write("- `mean-vector norm` is a window-level gravity/pose proxy when acceleration includes gravity.\n")
        f.write("- `dynamic RMS` is the residual motion energy after subtracting each window's mean vector.\n")
        f.write("- Compare static classes first. If Arduino Standing has dynamic energy closer to WISDM Walking than to WISDM Standing, the live Standing-to-Walking failure is likely not solved by orientation augmentation alone.\n")


def run_axis_eda(
    config_path: str | Path,
    *,
    output_dir: str | Path = "reports/m3/axis_eda",
    window_size: int | None = None,
) -> dict[str, Any]:
    config_path = Path(config_path)
    cfg = load_m3_config(config_path)
    window_size = int(
        window_size
        or cfg.get("paper_protocol", {}).get("wisdm_window_override", cfg["window_size_default"])
    )
    root = Path(output_dir)

    sample_rows: list[dict[str, Any]] = []
    window_rows: list[dict[str, Any]] = []
    dominant_rows: list[dict[str, Any]] = []
    meta: dict[str, dict[str, Any]] = {}
    for domain in ("wisdm", "arduino"):
        df, domain_meta = _prepare_domain(cfg, domain)
        meta[domain] = domain_meta
        sample_rows.extend(_sample_summary(df, domain))
        domain_window_rows, domain_dominant_rows = _window_summary(df, cfg, domain, window_size)
        window_rows.extend(domain_window_rows)
        dominant_rows.extend(domain_dominant_rows)

    sample_csv = root / "sample_axis_summary.csv"
    window_csv = root / "window_axis_summary.csv"
    dominant_csv = root / "dominant_axis_summary.csv"
    report_md = root / "axis_eda_report.md"
    _write_csv(sample_csv, sample_rows)
    _write_csv(window_csv, window_rows)
    _write_csv(dominant_csv, dominant_rows)
    _write_markdown(
        report_md,
        config_path=config_path,
        window_size=window_size,
        sample_rows=sample_rows,
        window_rows=window_rows,
        meta=meta,
    )
    return {
        "sample_csv": str(sample_csv),
        "window_csv": str(window_csv),
        "dominant_csv": str(dominant_csv),
        "report_md": str(report_md),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run M3 axis-level WISDM/Arduino EDA")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/m3/E04_wisdm_to_g_arduino_g.yaml"),
        help="M3 config used for unit/sampling/window settings.",
    )
    parser.add_argument("--output-dir", type=Path, default=Path("reports/m3/axis_eda"))
    parser.add_argument("--window-size", type=int, default=None)
    args = parser.parse_args()

    out = run_axis_eda(args.config, output_dir=args.output_dir, window_size=args.window_size)
    for key, value in out.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
