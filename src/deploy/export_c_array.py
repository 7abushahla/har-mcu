"""Convert a TFLite binary model into C/C++ source for TFLM."""

from __future__ import annotations

import argparse
from pathlib import Path


def _bytes_to_c_array(data: bytes, columns: int = 12) -> str:
    parts = []
    for i, b in enumerate(data):
        if i % columns == 0:
            parts.append("  ")
        parts.append(f"0x{b:02x}")
        if i != len(data) - 1:
            parts.append(", ")
        if (i + 1) % columns == 0:
            parts.append("\n")
    if not parts or parts[-1] != "\n":
        parts.append("\n")
    return "".join(parts)


def export_c_array(tflite_path: str, out_dir: str, var_name: str = "g_model_data") -> dict[str, str | int]:
    in_path = Path(tflite_path)
    if not in_path.exists():
        raise FileNotFoundError(f"TFLite file not found: {in_path}")

    out_dir_path = Path(out_dir)
    out_dir_path.mkdir(parents=True, exist_ok=True)

    data = in_path.read_bytes()
    arr = _bytes_to_c_array(data)

    header_path = out_dir_path / "model_data.h"
    source_path = out_dir_path / "model_data.cc"

    header_path.write_text(
        "\n".join(
            [
                "#pragma once",
                "",
                "#include <cstdint>",
                "",
                f"extern const unsigned char {var_name}[];",
                f"extern const unsigned int {var_name}_len;",
                "",
            ]
        ),
        encoding="utf-8",
    )

    source_path.write_text(
        "\n".join(
            [
                '#include "model_data.h"',
                "",
                f"alignas(16) const unsigned char {var_name}[] = {{",
                arr.rstrip("\n"),
                "};",
                f"const unsigned int {var_name}_len = {len(data)};",
                "",
            ]
        ),
        encoding="utf-8",
    )

    return {
        "header": str(header_path),
        "source": str(source_path),
        "bytes": len(data),
        "var_name": var_name,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Export TFLite to C array")
    parser.add_argument("--tflite", required=True, help="Path to .tflite file")
    parser.add_argument("--out-dir", default="deploy/common", help="Output directory")
    parser.add_argument("--var-name", default="g_model_data", help="C variable name")
    args = parser.parse_args()

    out = export_c_array(args.tflite, args.out_dir, var_name=args.var_name)
    for k, v in out.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
