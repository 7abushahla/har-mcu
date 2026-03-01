"""Run baseline sweep across multiple window sizes."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd

from src.data.build_dataset import build_dataset_for_protocol
from src.eval.eval_baseline import evaluate_baseline_for_protocol
from src.train.train_baseline import train_baseline_for_protocol
from src.utils.config import apply_common_overrides, build_parser, ensure_path_dirs, load_yaml


def run_sweep_for_protocol(cfg: dict[str, Any], protocol: str) -> dict[str, str]:
    ensure_path_dirs(cfg)

    rows: list[dict[str, float | int | str]] = []
    for window_size in cfg.get("window_sizes_sweep", []):
        ws = int(window_size)
        print(f"[sweep] protocol={protocol} window_size={ws}")
        build_dataset_for_protocol(cfg, ws, protocol)
        train_baseline_for_protocol(cfg, ws, protocol)
        metrics = evaluate_baseline_for_protocol(cfg, ws, protocol)
        rows.append(
            {
                "protocol": protocol,
                "window_size": ws,
                "accuracy": float(metrics["accuracy"]),
                "macro_f1": float(metrics["macro_f1"]),
            }
        )

    df = pd.DataFrame(rows).sort_values("window_size")

    reports_dir = Path(cfg["paths"]["reports_dir"])
    reports_dir.mkdir(parents=True, exist_ok=True)

    csv_path = reports_dir / f"window_sweep_P{protocol}.csv"
    png_path = reports_dir / f"window_sweep_P{protocol}.png"
    md_path = reports_dir / f"window_sweep_P{protocol}.md"

    df.to_csv(csv_path, index=False)

    plt.figure(figsize=(8, 5))
    plt.plot(df["window_size"], df["accuracy"], marker="o", label="Accuracy")
    plt.plot(df["window_size"], df["macro_f1"], marker="s", label="Macro-F1")
    plt.xlabel("Window size")
    plt.ylabel("Score")
    plt.title(f"Window Sweep ({protocol})")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(png_path)
    plt.close()

    best_row = df.sort_values("accuracy", ascending=False).iloc[0]
    with md_path.open("w", encoding="utf-8") as f:
        f.write(f"# Window Size Sweep ({protocol})\n\n")
        f.write(f"- CSV: `{csv_path}`\n")
        f.write(f"- Plot: `{png_path}`\n")
        f.write(
            f"- Best by accuracy: T={int(best_row['window_size'])}, accuracy={float(best_row['accuracy']):.4f}, macro-F1={float(best_row['macro_f1']):.4f}\n\n"
        )
        f.write("## Results\n\n")
        try:
            f.write(df.to_markdown(index=False))
        except Exception:
            f.write("```\n")
            f.write(df.to_string(index=False))
            f.write("\n```\n")

    return {"csv": str(csv_path), "png": str(png_path), "md": str(md_path)}


def main() -> None:
    parser = build_parser("Run baseline window size sweep")
    args = parser.parse_args()
    cfg = apply_common_overrides(load_yaml(args.config), args)

    for protocol in cfg.get("split_protocols", ["random_stratified"]):
        out = run_sweep_for_protocol(cfg, protocol)
        print(f"Sweep complete protocol={protocol}")
        for k, v in out.items():
            print(f"  - {k}: {v}")


if __name__ == "__main__":
    main()
