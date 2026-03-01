"""Export normalization stats JSON to Arduino header."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def export_norm_header(norm_json: str, out_path: str) -> dict[str, str]:
    payload = json.loads(Path(norm_json).read_text(encoding="utf-8"))
    mean = payload["mean"]
    std = payload["std"]

    text = "\n".join(
        [
            "#pragma once",
            "",
            "static constexpr float kNormMean[3] = {" + ", ".join(f"{x:.8f}f" for x in mean) + "};",
            "static constexpr float kNormStd[3] = {" + ", ".join(f"{x:.8f}f" for x in std) + "};",
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
