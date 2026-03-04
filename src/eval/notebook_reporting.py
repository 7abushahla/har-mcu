"""Shared notebook reporting utilities for paper replication notebooks."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.eval.evaluate_model import evaluate_model_for_protocol
from src.eval.paper_comparison import build_paper_comparison_rows
from src.utils.artifacts import model_ckpt_path, split_npz_path


def _read_json_if_exists(path: str | Path | None) -> dict[str, Any]:
    if not path:
        return {}
    p = Path(path)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def build_run_rows_df(out: dict[str, Any]) -> pd.DataFrame:
    return pd.DataFrame(out.get("rows", []))


def build_model_size_summary_df(rows: list[dict[str, Any]]) -> pd.DataFrame:
    summary_rows = [
        {
            "protocol": row.get("protocol"),
            "fp32_model_size_kb": row.get("fp32_model_size_kb"),
            "ptq_model_size_kb": row.get("ptq_model_size_kb"),
            "qat_model_size_kb": row.get("qat_model_size_kb"),
            "fp32_tflite_status": row.get("fp32_tflite_status"),
            "fp32_tflite_model": row.get("fp32_tflite_model"),
        }
        for row in rows
    ]
    return pd.DataFrame(
        summary_rows,
        columns=[
            "protocol",
            "fp32_model_size_kb",
            "ptq_model_size_kb",
            "qat_model_size_kb",
            "fp32_tflite_status",
            "fp32_tflite_model",
        ],
    )


def build_ptq_operator_visibility(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[str]]:
    visibility: list[dict[str, Any]] = []
    warnings: list[str] = []
    for row in rows:
        protocol = str(row.get("protocol"))
        ptq_eval_payload = _read_json_if_exists(row.get("ptq_metrics_json"))
        ptq_report_payload = _read_json_if_exists(row.get("ptq_report_json"))

        interpreter_ops = sorted(set(ptq_eval_payload.get("interpreter_ops", []) or []))
        tflm_ops = sorted(set(ptq_report_payload.get("tflm_ops", []) or []))
        only_interpreter = sorted(set(interpreter_ops) - set(tflm_ops))
        only_tflm = sorted(set(tflm_ops) - set(interpreter_ops))

        if only_interpreter or only_tflm:
            warnings.append(
                f"[{protocol}] op list mismatch (non-fatal): "
                f"only_interpreter={len(only_interpreter)}, only_tflm={len(only_tflm)}"
            )

        visibility.append(
            {
                "protocol": protocol,
                "interpreter_ops": interpreter_ops,
                "tflm_ops": tflm_ops,
                "only_interpreter": only_interpreter,
                "only_tflm": only_tflm,
            }
        )
    return visibility, warnings


def build_strict_deploy_table(
    rows: list[dict[str, Any]],
) -> tuple[pd.DataFrame, bool, list[str]]:
    strict_rows: list[dict[str, Any]] = []
    legacy_artifact_detected = False
    summary_lines: list[str] = []

    for row in rows:
        protocol = str(row.get("protocol"))
        ptq_status = row.get("ptq_status")
        qat_status = row.get("qat_status")
        summary_lines.append(f"[{protocol}] ptq_status={ptq_status} | qat_status={qat_status}")

        for tier, row_status, report_key in (
            ("PTQ", ptq_status, "ptq_report_json"),
            ("QAT", qat_status, "qat_report_json"),
        ):
            payload = _read_json_if_exists(row.get(report_key))
            if payload and (
                payload.get("allowed_ops_profile") is None or "allowed_ops_used" not in payload
            ):
                legacy_artifact_detected = True

            unsupported = payload.get("unsupported_ops_micro_mutable")
            if unsupported is None:
                unsupported = payload.get("unsupported_ops_profile")
            if unsupported is None:
                unsupported = payload.get("unsupported_ops", [])
            unsupported = unsupported or []
            unsupported_text = ", ".join(unsupported) if isinstance(unsupported, list) and unsupported else None

            status_from_report = payload.get(
                f"{tier.lower()}_status",
                payload.get("status", row_status),
            )
            allowed_profile = payload.get("allowed_ops_profile")
            err = payload.get("error")
            full_integer_io = payload.get("full_integer_io")
            tflm_compatible = payload.get("tflm_compatible")
            scope = payload.get("compatibility_scope", "micro_mutable_main")
            possibly_upstream = payload.get("possibly_supported_upstream_tflm", []) or []
            unsupported_ref = payload.get("unsupported_in_reference", []) or []

            strict_rows.append(
                {
                    "protocol": protocol,
                    "tier": tier,
                    "status": status_from_report,
                    "full_integer_io": full_integer_io,
                    "tflm_compatible": tflm_compatible,
                    "allowed_ops_profile": allowed_profile,
                    "compatibility_scope": scope,
                    "unsupported_ops_micro_mutable": unsupported_text,
                    "possibly_supported_upstream_tflm": ", ".join(possibly_upstream)
                    if possibly_upstream
                    else None,
                    "unsupported_in_reference": ", ".join(unsupported_ref) if unsupported_ref else None,
                    "error": err,
                }
            )

            if row_status == "failed":
                if not payload:
                    summary_lines.append(f"  {tier} failed (report missing)")
                else:
                    summary_lines.append(
                        f"  {tier} failed under compatibility_scope={scope}; "
                        f"unsupported_ops={unsupported}"
                    )
                    if err:
                        summary_lines.append(f"    reason: {err}")

    return pd.DataFrame(strict_rows), legacy_artifact_detected, summary_lines


def build_notebook_comparison_df(cfg: dict[str, Any], out: dict[str, Any]) -> pd.DataFrame:
    paper_targets = cfg.get("experiment", {}).get("paper_targets", {}) or {}
    rows = build_paper_comparison_rows(out.get("rows", []), paper_targets=paper_targets)
    return pd.DataFrame(rows).reset_index(drop=True)


def build_reproducibility_drift_df(
    cfg: dict[str, Any],
    out: dict[str, Any],
    *,
    drift_tol: float,
) -> pd.DataFrame:
    drift_rows: list[dict[str, Any]] = []
    paper_reports_dir = Path(cfg["paths"]["reports_dir"]) / cfg["experiment"]["paper_slug"]

    for row in out.get("rows", []):
        protocol = str(row["protocol"])
        window_size = int(row["window_size"])
        run_id = str(row["run_id"])
        variant = str(row["variant"])
        split_path = split_npz_path(cfg["paths"]["processed_dir"], window_size, protocol)

        split_hash = None
        if split_path.exists():
            with np.load(split_path, allow_pickle=True) as npz:
                if "split_hash" in npz:
                    raw_hash = npz["split_hash"]
                    split_hash = raw_hash.item() if hasattr(raw_hash, "item") else str(raw_hash)

        checkpoint = model_ckpt_path(
            cfg["paths"]["checkpoints_dir"],
            model_name=variant,
            window_size=window_size,
            protocol=protocol,
            run_id=run_id,
        )
        repeat_out = evaluate_model_for_protocol(
            cfg,
            model_path=str(checkpoint),
            protocol=protocol,
            window_size=window_size,
            run_id=run_id,
            reports_dir_override=paper_reports_dir,
        )
        repeat_metrics = _read_json_if_exists(repeat_out["metrics_json"])
        first_acc = float(row["accuracy"])
        repeat_acc = float(repeat_metrics["accuracy"])
        abs_drift = abs(repeat_acc - first_acc)
        drift_rows.append(
            {
                "protocol": protocol,
                "split_hash": split_hash,
                "baseline_acc_first": first_acc,
                "baseline_acc_repeat": repeat_acc,
                "abs_drift": abs_drift,
                "status": "PASS" if abs_drift <= drift_tol else "WARN",
            }
        )

    return pd.DataFrame(drift_rows)


def _plot_accuracy(comp_df: pd.DataFrame) -> None:
    rows = comp_df[comp_df["accuracy"].notna()].copy()
    if rows.empty:
        print("(No accuracy rows available for comparison chart.)")
        return

    labels = [
        f"{r.pipeline.replace('(', '').replace(')', '').strip()}\n{r.protocol}\n{r.model}"
        for r in rows.itertuples()
    ]
    accs = rows["accuracy"].astype(float).tolist()

    colors = []
    for r in rows.itertuples():
        if r.pipeline == "paper target":
            if r.model == "baseline float":
                colors.append("#9e9e9e")
            elif r.model == "PTQ int8":
                colors.append("#bdbdbd")
            else:
                colors.append("#d9d9d9")
        else:
            if r.model == "baseline float":
                colors.append("#1f77b4")
            elif r.model == "PTQ int8":
                colors.append("#ff7f0e")
            else:
                colors.append("#2ca02c")

    fig, ax = plt.subplots(figsize=(max(10, len(rows) * 1.4), 5.6))
    bars = ax.bar(labels, accs, color=colors, edgecolor="white", width=0.6)

    baseline_target = rows[(rows["pipeline"] == "paper target") & (rows["model"] == "baseline float")]
    ptq_target = rows[(rows["pipeline"] == "paper target") & (rows["model"] == "PTQ int8")]
    if not baseline_target.empty and pd.notna(baseline_target.iloc[0]["accuracy"]):
        v = float(baseline_target.iloc[0]["accuracy"])
        ax.axhline(v, color="#1f77b4", linestyle="--", linewidth=1.0, label=f"Paper target baseline ({v:.4f})")
    if not ptq_target.empty and pd.notna(ptq_target.iloc[0]["accuracy"]):
        v = float(ptq_target.iloc[0]["accuracy"])
        ax.axhline(v, color="#ff7f0e", linestyle="--", linewidth=1.0, label=f"Paper target PTQ ({v:.4f})")

    for bar, acc in zip(bars, accs):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.002, f"{acc:.4f}", ha="center", va="bottom", fontsize=8)

    ax.set_ylim(max(0.0, min(accs) - 0.05), 1.02)
    ax.set_ylabel("Accuracy")
    ax.set_title("Paper Target vs WISDM Replication — Accuracy comparison (baseline/PTQ/QAT)")
    ax.text(
        0.01,
        0.02,
        "Note: QAT paper-target values may be unavailable; those are shown as replication-only rows.",
        transform=ax.transAxes,
        fontsize=8,
        ha="left",
        va="bottom",
        bbox={"facecolor": "white", "alpha": 0.85, "edgecolor": "none"},
    )
    ax.legend(fontsize=8)
    ax.grid(axis="y", alpha=0.4)
    plt.xticks(fontsize=7.5)
    plt.tight_layout()
    plt.show()


def _plot_model_size(comp_df: pd.DataFrame) -> None:
    rows = comp_df[
        (comp_df["pipeline"] == "WISDM replication")
        & (comp_df["model"].isin({"baseline float", "PTQ int8", "QAT int8"}))
        & (comp_df["model_size_kb"].notna())
    ].copy()
    if rows.empty:
        return
    size_df = pd.DataFrame(
        [(r.pipeline, r.protocol, r.model, r.model_size_kb) for r in rows.itertuples()],
        columns=["pipeline", "protocol", "model", "model_size_kb"],
    )
    from IPython.display import display

    display(size_df.style.format({"model_size_kb": "{:.2f} KB"}).set_caption("Table 2 — Model size (FP32/PTQ/QAT)"))


def _plot_latency(comp_df: pd.DataFrame) -> None:
    rows = comp_df[
        (comp_df["pipeline"] == "WISDM replication")
        & (comp_df["model"].isin({"PTQ int8", "QAT int8"}))
        & (comp_df["inference_latency_ms_median"].notna())
    ].copy()
    if rows.empty:
        return
    labels = [f"{r.protocol}\n{r.model}" for r in rows.itertuples()]
    x = np.arange(len(rows))
    med = rows["inference_latency_ms_median"].astype(float).to_numpy()
    p95 = rows["inference_latency_ms_p95"].astype(float).to_numpy()
    w = 0.38
    fig, ax = plt.subplots(figsize=(max(8, len(rows) * 1.2), 5.0))
    ax.bar(x - w / 2, med, width=w, label="median (ms)", color="#59a14f")
    ax.bar(x + w / 2, p95, width=w, label="p95 (ms)", color="#e15759")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("Latency (ms/sample)")
    ax.set_title("TFLite Inference Latency (Median + p95)")
    ax.legend()
    ax.grid(axis="y", alpha=0.35)
    plt.tight_layout()
    plt.show()


def render_visual_sections(
    cfg: dict[str, Any],
    out: dict[str, Any],
    *,
    rows_df: pd.DataFrame,
    ptq_visibility: list[dict[str, Any]],
    ptq_warnings: list[str],
    strict_df: pd.DataFrame,
    strict_summary_lines: list[str],
    legacy_artifact_detected: bool,
    comparison_df: pd.DataFrame,
    reproducibility_df: pd.DataFrame,
) -> None:
    from IPython.display import Image, Markdown, display

    display(rows_df)
    model_size_df = build_model_size_summary_df(out.get("rows", []))
    if not model_size_df.empty:
        display(
            model_size_df.style.format(
                {
                    "fp32_model_size_kb": lambda v: f"{float(v):.2f} KB"
                    if v is not None and pd.notna(v)
                    else "—",
                    "ptq_model_size_kb": lambda v: f"{float(v):.2f} KB"
                    if v is not None and pd.notna(v)
                    else "—",
                    "qat_model_size_kb": lambda v: f"{float(v):.2f} KB"
                    if v is not None and pd.notna(v)
                    else "—",
                    "fp32_tflite_status": lambda v: str(v) if v is not None else "—",
                    "fp32_tflite_model": lambda v: str(v) if v else "—",
                }
            ).set_caption("Model Size Summary (FP32 float .tflite, PTQ INT8, QAT INT8)")
        )
        print("Note: fp32_model_size_kb is measured from exported float .tflite per protocol.")

    print("\nPTQ operator visibility (per protocol):")
    print("- interpreter_ops: delegate-free runtime ops from PTQ TFLite evaluation metrics")
    print("- tflm_ops: flatbuffer ops used by strict deploy-gate compatibility check")
    for item in ptq_visibility:
        print(f"\n[{item['protocol']}]")
        print(f"  interpreter_ops ({len(item['interpreter_ops'])}): {item['interpreter_ops']}")
        print(f"  tflm_ops       ({len(item['tflm_ops'])}): {item['tflm_ops']}")
    for warning in ptq_warnings:
        print(f"  [WARN] {warning}")

    print("\nStrict deploy-gate status summary:")
    for line in strict_summary_lines:
        print(line)

    print("\nStrict Deploy-Gate Details (from export reports):")
    if not strict_df.empty:
        display(
            strict_df.style.format(
                {
                    "status": lambda v: str(v) if v is not None else "—",
                    "full_integer_io": lambda v: str(v) if v is not None else "—",
                    "tflm_compatible": lambda v: str(v) if v is not None else "—",
                    "allowed_ops_profile": lambda v: str(v) if v is not None else "—",
                    "compatibility_scope": lambda v: str(v) if v is not None else "—",
                    "unsupported_ops_micro_mutable": lambda v: v if v else "—",
                    "possibly_supported_upstream_tflm": lambda v: v if v else "—",
                    "unsupported_in_reference": lambda v: v if v else "—",
                    "error": lambda v: v if v else "—",
                }
            ).set_caption("Strict deploy-gate details per protocol/tier (PTQ, QAT)")
        )
    else:
        print("(No PTQ/QAT strict report rows found.)")

    if legacy_artifact_detected:
        print("[WARN] Legacy artifact detected; rerun end-to-end to refresh strict deploy-gate outputs.")
    print(
        "Note: if you changed model_variant/run_id, compare only current run rows and artifacts. "
        "Older files may still exist under reports/<paper_slug>/."
    )

    display(
        comparison_df.style.format(
            {
                "accuracy": lambda v: f"{v:.4f}" if v is not None and pd.notna(v) else "—",
                "macro_f1": lambda v: f"{v:.4f}" if v is not None and pd.notna(v) else "—",
                "model_size_kb": lambda v: f"{v:.2f}" if v is not None and pd.notna(v) else "—",
                "training_time_sec": lambda v: f"{v:.2f}s" if v is not None and pd.notna(v) else "—",
                "inference_latency_ms_median": lambda v: f"{v:.3f}ms" if v is not None and pd.notna(v) else "—",
                "inference_latency_ms_p95": lambda v: f"{v:.3f}ms" if v is not None and pd.notna(v) else "—",
                "acc_delta_vs_target": lambda v: f"{v:+.4f}" if v is not None and pd.notna(v) else "—",
            }
        )
        .applymap(
            lambda v: "color: green"
            if isinstance(v, float) and v > 0
            else ("color: red" if isinstance(v, float) and v < -0.0001 else ""),
            subset=["acc_delta_vs_target"],
        )
        .set_caption(
            "Table 1 — Accuracy, macro F1, model size, timing, and accuracy delta vs paper target (baseline/PTQ/QAT)"
        )
    )
    print("Note: Paper-target QAT may be unavailable in source papers; QAT rows here are replication extensions where target is N/A.")
    _plot_accuracy(comparison_df)
    _plot_model_size(comparison_df)
    _plot_latency(comparison_df)

    print("\nReproducibility drift — WISDM replication (repeat evaluation on saved checkpoint):")
    if not reproducibility_df.empty:
        display(
            reproducibility_df[
                [
                    "protocol",
                    "split_hash",
                    "baseline_acc_first",
                    "baseline_acc_repeat",
                    "abs_drift",
                    "status",
                ]
            ]
            .style.format(
                {
                    "baseline_acc_first": "{:.4f}",
                    "baseline_acc_repeat": "{:.4f}",
                    "abs_drift": "{:.2e}",
                }
            )
            .applymap(
                lambda v: "color: green" if v == "PASS" else ("color: orange" if v == "WARN" else ""),
                subset=["status"],
            )
            .set_caption("Table 3 — Reproducibility drift (two consecutive FP32 evaluations)")
        )
    else:
        print("(No reproducibility rows available.)")

    for row in out.get("rows", []):
        display(Markdown(f"### Protocol: `{row.get('protocol')}`"))
        for label, key in (
            ("FP32 training curve", "fp32_curve_png"),
            ("QAT training curve", "qat_curve_png"),
            ("FP32 confusion", "fp32_confusion_plot"),
            ("PTQ confusion", "ptq_confusion_plot"),
            ("QAT confusion", "qat_confusion_plot"),
        ):
            p = row.get(key)
            if p and Path(p).exists():
                display(Markdown(f"**{label}**"))
                display(Image(filename=str(p), width=760))

    for row in out.get("rows", []):
        display(Markdown(f"### Classification Report Snippets — `{row.get('protocol')}`"))
        for tier, key in (("FP32", "fp32_metrics_json"), ("PTQ", "ptq_metrics_json"), ("QAT", "qat_metrics_json")):
            payload = _read_json_if_exists(row.get(key))
            if not payload:
                continue
            report = payload.get("classification_report", {})
            macro = report.get("macro avg", {}) if isinstance(report, dict) else {}
            weighted = report.get("weighted avg", {}) if isinstance(report, dict) else {}
            print(f"{tier}: macro_f1={macro.get('f1-score')}, weighted_f1={weighted.get('f1-score')}")

    cmp = out.get("comparison_exports", {})
    if cmp.get("csv") and Path(cmp["csv"]).exists():
        display(Markdown("## Saved Comparison CSV Snapshot"))
        display(pd.read_csv(cmp["csv"]))
    for key in ("accuracy_png", "size_png", "latency_png"):
        p = cmp.get(key)
        if p and Path(p).exists():
            display(Image(filename=str(p), width=920))

    master_csv = Path(cfg["paths"]["reports_dir"]) / "results_master.csv"
    if master_csv.exists():
        df_master = pd.read_csv(master_csv)
        display(Markdown("## Master Results Snapshot"))
        display(df_master[df_master["paper_slug"] == cfg["experiment"]["paper_slug"]])

    print("Saved outputs root:", Path(cfg["paths"]["reports_dir"]) / cfg["experiment"]["paper_slug"])


def render_paper_notebook_report(
    cfg: dict[str, Any],
    out: dict[str, Any],
    *,
    drift_tol: float = 1e-9,
) -> dict[str, Any]:
    rows_df = build_run_rows_df(out)
    ptq_visibility, ptq_warnings = build_ptq_operator_visibility(out.get("rows", []))
    strict_df, legacy_detected, strict_summary_lines = build_strict_deploy_table(out.get("rows", []))
    comparison_df = build_notebook_comparison_df(cfg, out)
    reproducibility_df = build_reproducibility_drift_df(cfg, out, drift_tol=drift_tol)

    render_visual_sections(
        cfg,
        out,
        rows_df=rows_df,
        ptq_visibility=ptq_visibility,
        ptq_warnings=ptq_warnings,
        strict_df=strict_df,
        strict_summary_lines=strict_summary_lines,
        legacy_artifact_detected=legacy_detected,
        comparison_df=comparison_df,
        reproducibility_df=reproducibility_df,
    )
    return {
        "rows_df": rows_df,
        "ptq_operator_visibility": ptq_visibility,
        "ptq_operator_warnings": ptq_warnings,
        "strict_deploy_df": strict_df,
        "legacy_artifact_detected": legacy_detected,
        "strict_summary_lines": strict_summary_lines,
        "comparison_df": comparison_df,
        "reproducibility_df": reproducibility_df,
    }
