"""Export normalization stats JSON to Arduino header."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def export_norm_header(norm_json: str, out_path: str) -> dict[str, str]:
    payload = json.loads(Path(norm_json).read_text(encoding="utf-8"))
    mean = payload["mean"]
    std = payload["std"]
    data = payload.get("data", {})
    unit = data.get("unit_transform", {})
    sampling = data.get("sampling", {})
    window_size = int(payload.get("window_size_samples", payload.get("window_size", 100)))
    sample_rate_hz = int(round(float(sampling.get("target_sample_rate_hz", 20))))
    apply_norm = 1 if bool(payload.get("inference_norm_applied", True)) else 0
    unit_pre_multiply = float(unit.get("pre_multiply", 1.0))
    unit_scale = float(unit.get("scale", 1.0))

    text = "\n".join(
        [
            "#pragma once",
            "",
            f"#define WINDOW_SIZE {window_size}",
            f"#define SAMPLE_RATE_HZ {sample_rate_hz}",
            f"#define APPLY_NORMALIZATION {apply_norm}",
            f"#define UNIT_PRE_MULTIPLY {unit_pre_multiply:.8f}f",
            f"#define UNIT_SCALE {unit_scale:.8f}f",
            "",
            "static constexpr float kNormMean[3] = {" + ", ".join(f"{x:.8f}f" for x in mean) + "};",
            "static constexpr float kNormStd[3] = {" + ", ".join(f"{x:.8f}f" for x in std) + "};",
            f'static constexpr const char* kNormalizationMode = "{payload.get("normalization_mode", "train_zscore")}";',
            f'static constexpr const char* kUnitMode = "{unit.get("unit_mode", "raw_no_conversion")}";',
            "",
        ]
    )
    p = Path(out_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return {"norm_header": str(p)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Export norm stats header")
    parser.add_argument("--norm-json", required=True)
    parser.add_argument("--out", default="deploy/common/norm_stats.h")
    args = parser.parse_args()
    out = export_norm_header(args.norm_json, args.out)
    for k, v in out.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
