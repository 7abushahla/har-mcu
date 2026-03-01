#!/usr/bin/env python3
"""Check core dependency versions and basic compatibility assumptions."""

from __future__ import annotations

import json
from packaging.version import Version


def _get_version(pkg: str) -> str:
    module = __import__(pkg)
    return getattr(module, "__version__", "unknown")


def main() -> None:
    checks = [
        ("tensorflow", "==2.14.1", lambda v: Version(v) == Version("2.14.1")),
        ("numpy", "<2", lambda v: Version(v) < Version("2")),
        ("pandas", ">=2.0", lambda v: Version(v) >= Version("2.0")),
        ("scipy", ">=1.10", lambda v: Version(v) >= Version("1.10")),
        ("sklearn", ">=1.3", lambda v: Version(v) >= Version("1.3")),
        (
            "tensorflow_model_optimization",
            "==0.8.0",
            lambda v: Version(v) == Version("0.8.0"),
        ),
    ]

    payload = {
        "expected": {module: rule for module, rule, _ in checks},
        "actual": {},
        "ok": True,
        "notes": [],
    }
    for module_name, rule, matcher in checks:
        try:
            actual = _get_version(module_name)
            payload["actual"][module_name] = actual
            if not matcher(actual):
                payload["ok"] = False
                payload["notes"].append(
                    f"Version mismatch for {module_name}: expected {rule}, got {actual}"
                )
        except Exception as exc:
            payload["ok"] = False
            payload["actual"][module_name] = f"error: {exc}"
            payload["notes"].append(f"Failed to import {module_name}: {exc}")

    with open("reports/version_check.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(json.dumps(payload, indent=2))
    raise SystemExit(0 if payload["ok"] else 1)


if __name__ == "__main__":
    main()
