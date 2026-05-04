"""Eval-only WISDM/Arduino test-set matrix for M3 artifacts."""

from __future__ import annotations

import argparse
import copy
import csv
import json
from pathlib import Path
from typing import Any

import numpy as np

from src.data.build_dataset import build_dataset_for_protocol
from src.eval.eval_tflite import evaluate_tflite
from src.m3.config import load_m3_config
from src.run_paper_experiment import _read_json
from src.utils.artifacts import (
    model_fp32_tflite_path,
    model_ptq_tflite_path,
    model_qat_tflite_path,
    model_slug,
    norm_stats_path,
)
from src.utils.markdown_tables import dataframe_to_pipe_markdown
from src.utils.repro import dump_json


EVAL_DOMAINS = ("wisdm", "arduino")
TIERS = ("fp32", "ptq", "qat")


def _experiment_code(cfg: dict[str, Any]) -> str:
    return str(cfg.get("m3", {}).get("experiment_id", "m3")).split("_", 1)[0]


def _format_artifact_suffix(cfg: dict[str, Any], suffix: str) -> str:
    exp = cfg.get("experiment", {})
    values = {
        "experiment_id": str(cfg.get("m3", {}).get("experiment_id", "")),
        "experiment_code": _experiment_code(cfg).lower(),
        "model_variant": model_slug(str(exp.get("model_variant", ""))),
        "run_id": model_slug(str(exp.get("run_id", ""))),
    }
    return suffix.format(**values)


def _append_path_suffix(cfg: dict[str, Any], suffix: str) -> None:
    if not suffix:
        return
    clean_suffix = suffix.strip("/")
    for key in (
        "processed_dir",
        "checkpoints_dir",
        "reports_dir",
        "models_tflite_dir",
        "deploy_common_dir",
    ):
        value = cfg.get("paths", {}).get(key)
        if value:
            cfg["paths"][key] = str(value).rstrip("/") + "/" + clean_suffix


def _apply_model_override(
    cfg: dict[str, Any],
    *,
    model_variant: str,
    run_id: str | None,
) -> None:
    exp = cfg.setdefault("experiment", {})
    original_variant = str(exp.get("model_variant", ""))
    exp["model_variant"] = str(model_variant)
    if run_id:
        exp["run_id"] = str(run_id)
    elif model_variant != original_variant:
        exp["run_id"] = f"{_experiment_code(cfg)}_{model_slug(model_variant)}_r0"


def _load_norm_stats(stats_file: Path) -> dict[str, Any]:
    with stats_file.open("r", encoding="utf-8") as f:
        stats = json.load(f)
    return {
        "mean": np.asarray(stats["mean"], dtype=np.float32),
        "std": np.asarray(stats["std"], dtype=np.float32),
    }


def _training_stats_dir(cfg: dict[str, Any]) -> Path:
    processed = Path(cfg["paths"]["processed_dir"])
    mode = str(cfg.get("m3", {}).get("transfer_mode", "source_only"))
    if mode == "zero_shot":
        return processed / "source_wisdm"
    if mode == "finetune":
        return processed / "finetune_arduino"
    return processed


def _domain_eval_cfg(
    cfg: dict[str, Any],
    *,
    eval_domain: str,
    output_root: Path,
) -> dict[str, Any]:
    out = copy.deepcopy(cfg)
    paths = out.setdefault("paths", {})
    paths["processed_dir"] = str(output_root / eval_domain)
    raw_key = f"{eval_domain}_raw_csv"
    if paths.get(raw_key):
        paths["raw_csv"] = paths[raw_key]

    data = out.setdefault("data", {})
    data["source"] = eval_domain
    data["train_domain"] = eval_domain
    data["eval_domain"] = eval_domain

    # Cross-eval should score artifacts, not spend time on latency sampling.
    out.setdefault("eval", {}).setdefault("tflite_timing", {})["enabled"] = False
    return out


def _build_domain_eval_dataset(
    cfg: dict[str, Any],
    *,
    eval_domain: str,
    window_size: int,
    protocol: str,
    output_root: Path,
    normalization_stats: dict[str, Any],
    normalization_stats_source: str,
) -> dict[str, Any]:
    eval_cfg = _domain_eval_cfg(cfg, eval_domain=eval_domain, output_root=output_root)
    build_dataset_for_protocol(
        eval_cfg,
        window_size=window_size,
        protocol=protocol,
        normalization_stats=normalization_stats,
        normalization_stats_source=normalization_stats_source,
    )
    return eval_cfg


def _artifact_paths(
    cfg: dict[str, Any],
    *,
    model_variant: str,
    window_size: int,
    protocol: str,
    run_id: str,
) -> dict[str, Path]:
    models_dir = cfg["paths"]["models_tflite_dir"]
    return {
        "fp32": model_fp32_tflite_path(
            models_dir,
            model_name=model_variant,
            window_size=window_size,
            protocol=protocol,
            run_id=run_id,
        ),
        "ptq": model_ptq_tflite_path(
            models_dir,
            model_name=model_variant,
            window_size=window_size,
            protocol=protocol,
            run_id=run_id,
        ),
        "qat": model_qat_tflite_path(
            models_dir,
            model_name=model_variant,
            window_size=window_size,
            protocol=protocol,
            run_id=run_id,
        ),
    }


def run_dual_domain_eval(
    *,
    config_path: str | Path,
    model_variant: str,
    augment_label: str,
    artifact_suffix: str,
    run_id: str | None = None,
    protocol: str = "random_stratified",
    output_dir: str | Path = "reports/m3/dual_domain_eval",
) -> dict[str, Any]:
    cfg = load_m3_config(config_path)
    _apply_model_override(cfg, model_variant=model_variant, run_id=run_id)
    formatted_suffix = _format_artifact_suffix(cfg, artifact_suffix)
    _append_path_suffix(cfg, formatted_suffix)

    exp_id = str(cfg.get("m3", {}).get("experiment_id"))
    exp_code = _experiment_code(cfg).lower()
    run_id_effective = str(cfg.get("experiment", {}).get("run_id"))
    window_size = int(cfg.get("paper_protocol", {}).get("wisdm_window_override", cfg["window_size_default"]))
    model_variant = str(cfg.get("experiment", {}).get("model_variant"))

    train_stats_dir = _training_stats_dir(cfg)
    stats_file = norm_stats_path(train_stats_dir, window_size, protocol)
    if not stats_file.exists():
        raise FileNotFoundError(f"Training normalization stats not found: {stats_file}")
    normalization_stats = _load_norm_stats(stats_file)

    out_root = Path(output_dir) / augment_label / model_slug(model_variant) / exp_code
    out_root.mkdir(parents=True, exist_ok=True)
    processed_eval_root = (
        Path("data/processed/m3")
        / exp_id
        / "dual_domain_eval"
        / augment_label
        / model_slug(model_variant)
        / exp_code
    )

    artifacts = _artifact_paths(
        cfg,
        model_variant=model_variant,
        window_size=window_size,
        protocol=protocol,
        run_id=run_id_effective,
    )
    missing = [str(path) for path in artifacts.values() if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing TFLite artifact(s): " + ", ".join(missing))

    rows: list[dict[str, Any]] = []
    for eval_domain in EVAL_DOMAINS:
        eval_cfg = _build_domain_eval_dataset(
            cfg,
            eval_domain=eval_domain,
            window_size=window_size,
            protocol=protocol,
            output_root=processed_eval_root,
            normalization_stats=normalization_stats,
            normalization_stats_source=f"model_train:{stats_file}",
        )
        for tier in TIERS:
            tag = f"{augment_label}_{tier}_{model_slug(model_variant)}_{exp_code}_{eval_domain}"
            eval_out = evaluate_tflite(
                eval_cfg,
                str(artifacts[tier]),
                window_size,
                protocol,
                tag=tag,
                reports_dir_override=out_root,
            )
            metrics = _read_json(eval_out["metrics_json"])
            rows.append(
                {
                    "experiment_id": exp_id,
                    "experiment_code": exp_code,
                    "model_variant": model_variant,
                    "augment_label": augment_label,
                    "artifact_suffix": formatted_suffix,
                    "run_id": run_id_effective,
                    "eval_domain": eval_domain,
                    "tier": tier,
                    "window_size": window_size,
                    "protocol": protocol,
                    "accuracy": float(metrics["accuracy"]),
                    "macro_f1": float(metrics["macro_f1"]),
                    "model_size_kb": float(metrics["model_size_kb"]),
                    "input_dtype": str(metrics["input_dtype"]),
                    "output_dtype": str(metrics["output_dtype"]),
                    "model_path": str(artifacts[tier]),
                    "metrics_json": eval_out["metrics_json"],
                    "report_md": eval_out["report_md"],
                    "processed_dir": str(eval_cfg["paths"]["processed_dir"]),
                    "normalization_stats": str(stats_file),
                }
            )

    json_path = out_root / "dual_domain_eval.json"
    csv_path = out_root / "dual_domain_eval.csv"
    md_path = out_root / "dual_domain_eval.md"
    payload = {
        "experiment_id": exp_id,
        "experiment_code": exp_code,
        "model_variant": model_variant,
        "augment_label": augment_label,
        "artifact_suffix": formatted_suffix,
        "run_id": run_id_effective,
        "rows": rows,
    }
    dump_json(json_path, payload)

    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    try:
        import pandas as pd

        df = pd.DataFrame(rows)
        table = dataframe_to_pipe_markdown(df)
    except Exception:
        table = ""
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# M3 Dual-Domain TFLite Evaluation\n\n")
        f.write(f"- Experiment: `{exp_id}`\n")
        f.write(f"- Model: `{model_variant}`\n")
        f.write(f"- Augmentation: `{augment_label}`\n")
        f.write(f"- Rows: `{len(rows)}`\n\n")
        if table:
            f.write(table)
            f.write("\n")

    return {
        "json": str(json_path),
        "csv": str(csv_path),
        "md": str(md_path),
        "rows": rows,
    }


def aggregate_dual_domain_eval(
    output_dir: str | Path = "reports/m3/dual_domain_eval",
) -> dict[str, Any]:
    root = Path(output_dir)
    paths = sorted(root.glob("*/*/*/dual_domain_eval.csv"))
    rows: list[dict[str, Any]] = []
    for path in paths:
        with path.open(encoding="utf-8", newline="") as f:
            rows.extend(dict(row, source_csv=str(path)) for row in csv.DictReader(f))

    root.mkdir(parents=True, exist_ok=True)
    out_csv = root / "dual_domain_eval_master.csv"
    out_md = root / "dual_domain_eval_master.md"
    if not rows:
        out_csv.write_text("", encoding="utf-8")
        out_md.write_text("# M3 dual-domain evaluation\n\n- Rows: `0`\n", encoding="utf-8")
        return {"csv": str(out_csv), "md": str(out_md), "rows": 0}

    fieldnames = list(rows[0].keys())
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    try:
        import pandas as pd

        df = pd.DataFrame(rows)
        table = dataframe_to_pipe_markdown(df)
    except Exception:
        table = ""
    with out_md.open("w", encoding="utf-8") as f:
        f.write("# M3 dual-domain evaluation master\n\n")
        f.write(f"- Rows: `{len(rows)}`\n")
        f.write(f"- Source CSVs: `{len(paths)}`\n\n")
        if table:
            f.write(table)
            f.write("\n")
    return {"csv": str(out_csv), "md": str(out_md), "rows": len(rows), "sources": len(paths)}


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, help="M3 config path")
    parser.add_argument("--model-variant", help="Model variant to evaluate")
    parser.add_argument("--augment-label", choices=["off", "on"], help="Augmentation condition label")
    parser.add_argument("--artifact-suffix", help="Artifact suffix used by the trained run")
    parser.add_argument("--run-id", default=None, help="Optional explicit run_id override")
    parser.add_argument("--protocol", default="random_stratified")
    parser.add_argument("--output-dir", type=Path, default=Path("reports/m3/dual_domain_eval"))
    parser.add_argument("--aggregate-only", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    if args.aggregate_only:
        out = aggregate_dual_domain_eval(args.output_dir)
        print(f"rows: {out['rows']}")
        print(f"csv: {out['csv']}")
        print(f"md: {out['md']}")
        return

    required = {
        "--config": args.config,
        "--model-variant": args.model_variant,
        "--augment-label": args.augment_label,
        "--artifact-suffix": args.artifact_suffix,
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        raise SystemExit(f"Missing required arguments: {', '.join(missing)}")

    out = run_dual_domain_eval(
        config_path=args.config,
        model_variant=args.model_variant,
        augment_label=args.augment_label,
        artifact_suffix=args.artifact_suffix,
        run_id=args.run_id,
        protocol=args.protocol,
        output_dir=args.output_dir,
    )
    print(f"rows: {len(out['rows'])}")
    print(f"csv: {out['csv']}")
    print(f"json: {out['json']}")


if __name__ == "__main__":
    main()
