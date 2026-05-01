"""Plot Pareto frontiers: model size (KB, TFLite / int8 path) vs quantized accuracy.

Reads `reports/m3/m3_experiment_master_all.csv` (or `--csv`).  For each selected
experiment + eval domain, draws all architectures and marks the **non-dominated**
set for (minimize size, maximize accuracy) using **PTQ** and/or **QAT** columns.

Rows with `ptq=failed` / `qat=failed` in `deploy_gate_status` are excluded from
that metric's Pareto (they are not valid int8 deploy points).

Examples::

  python scripts/plot_m3_pareto_int8.py
  python scripts/plot_m3_pareto_int8.py --experiments E09_wisdm_pretrain_arduino_finetune E10_arduino_from_scratch
  python scripts/plot_m3_pareto_int8.py --eval-domain wisdm --experiments E00_wisdm_m2_anchor

Outputs PNGs under `reports/m3/figures/` by default.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402


def _short_name(model_variant: str) -> str:
    m = {
        "daghero_cnn_2layer_conv2d": "daghero",
        "deepconv_lstm_conv2d": "deepconv",
        "repmobile_folded_conv2d": "repmobile",
        "tcn_attention_har_teacher_conv2d": "tcn_att",
        "tcn_inception_conv2d": "tcn_inc",
        "xtinyhar_student_conv2d": "xth",
        "xtinyhar_student_conv2d_relu": "xth_relu",
    }
    return m.get(model_variant, model_variant[:12])


def _gate_ok(status: str, key: str) -> bool:
    if not isinstance(status, str):
        return False
    return f"{key}=failed" not in status


def pareto_mask(size: np.ndarray, acc: np.ndarray) -> np.ndarray:
    """True for non-dominated points: minimize size, maximize acc."""
    n = len(size)
    keep = np.ones(n, dtype=bool)
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if (
                size[j] <= size[i]
                and acc[j] >= acc[i]
                and (size[j] < size[i] or acc[j] > acc[i])
            ):
                keep[i] = False
                break
    return keep


def plot_panel(
    ax: plt.Axes,
    sub: pd.DataFrame,
    metric: str,
    title: str,
) -> None:
    acc_col = f"{metric}_accuracy"
    if acc_col not in sub.columns or sub.empty:
        ax.text(0.5, 0.5, "no data", ha="center", va="center", transform=ax.transAxes)
        ax.set_title(title)
        return

    sub = sub.copy()
    sub["_ok"] = sub["deploy_gate_status"].apply(lambda s: _gate_ok(s, metric))
    usable = sub[sub["_ok"] & sub[acc_col].notna() & sub["model_size_kb"].notna()]
    if usable.empty:
        ax.text(0.5, 0.5, f"no {metric.upper()} rows", ha="center", va="center", transform=ax.transAxes)
        ax.set_title(title)
        return

    sizes = usable["model_size_kb"].to_numpy(dtype=float)
    accs = usable[acc_col].to_numpy(dtype=float)
    names = usable["model_variant"].map(_short_name).tolist()
    mask = pareto_mask(sizes, accs)

    ax.scatter(sizes[~mask], accs[~mask], s=55, c="#94a3b8", edgecolors="white", linewidths=0.8, zorder=2)
    ax.scatter(sizes[mask], accs[mask], s=95, c="#2563eb", edgecolors="white", linewidths=1.0, zorder=3)

    order = np.argsort(sizes[mask])
    sf = sizes[mask][order]
    af = accs[mask][order]
    ax.plot(sf, af, color="#1d4ed8", linewidth=1.6, alpha=0.85, zorder=1, label="Pareto front")

    for i, lbl in enumerate(names):
        if mask[i]:
            ax.annotate(
                lbl,
                (sizes[i], accs[i]),
                textcoords="offset points",
                xytext=(4, 4),
                fontsize=8,
                color="#1e3a8a",
            )

    ax.set_xlabel("Model size (KB)")
    ax.set_ylabel(f"{metric.upper()} accuracy (int8)")
    ax.set_title(title, fontsize=10)
    ax.grid(True, alpha=0.35)
    ax.legend(loc="lower right", fontsize=8)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--csv", type=Path, default=Path("reports/m3/m3_experiment_master_all.csv"))
    p.add_argument("--out-dir", type=Path, default=Path("reports/m3/figures"))
    p.add_argument(
        "--eval-domain",
        default="arduino",
        choices=("arduino", "wisdm"),
        help="Which eval_domain rows to plot (default: arduino).",
    )
    p.add_argument(
        "--experiments",
        nargs="+",
        default=[
            "E09_wisdm_pretrain_arduino_finetune",
            "E10_arduino_from_scratch",
            "E11_wisdm_pretrain_arduino_finetune_T50",
            "E12_arduino_from_scratch_T50",
        ],
        help="experiment_id values (one subplot column each).",
    )
    p.add_argument("--metrics", nargs="+", default=("ptq", "qat"), choices=("ptq", "qat"))
    args = p.parse_args()

    root = Path(__file__).resolve().parent.parent
    csv_path = args.csv if args.csv.is_absolute() else root / args.csv
    out_dir = args.out_dir if args.out_dir.is_absolute() else root / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(csv_path)
    df = df[df["eval_domain"] == args.eval_domain].copy()

    n_exp = len(args.experiments)
    n_met = len(args.metrics)
    fig_w = max(10.0, 3.2 * n_exp)
    fig_h = 3.8 * n_met
    fig, axes = plt.subplots(n_met, n_exp, figsize=(fig_w, fig_h), squeeze=False)

    for mi, metric in enumerate(args.metrics):
        for ei, exp in enumerate(args.experiments):
            ax = axes[mi][ei]
            sub = df[df["experiment_id"] == exp]
            short_exp = re.sub(r"^E\d+_", "", exp)[:28]
            w = int(sub["window_size_samples"].iloc[0]) if len(sub) else "?"
            title = f"{exp}\nT={w} · {args.eval_domain}"
            plot_panel(ax, sub, metric, title)

    fig.suptitle(
        f"M3 Pareto: size vs int8 ({'/'.join(m.upper() for m in args.metrics)}) — {args.eval_domain}",
        fontsize=12,
        y=1.02,
    )
    fig.tight_layout()
    slug_parts: list[str] = []
    for e in args.experiments:
        m = re.match(r"(E\d+)_", e)
        slug_parts.append(m.group(1) if m else re.sub(r"[^\w]+", "_", e)[:16])
    slug = "_".join(slug_parts)
    out_png = out_dir / f"pareto_int8_{args.eval_domain}_{slug}.png"
    fig.savefig(out_png, dpi=160, bbox_inches="tight")
    plt.close(fig)
    print(out_png)


if __name__ == "__main__":
    main()
