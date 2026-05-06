#!/usr/bin/env python3
"""Run the milestone M3 header exporter from inside har-mcu.

This wrapper forwards all CLI args to:
  ../project-milestone-3-group-2/scripts/export_m3_deploy_headers.py

If --har-mcu is not provided, it injects the current har-mcu root so relative
paths resolve correctly when invoked from this repository.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    har_root = Path(__file__).resolve().parents[1]
    milestones_root = har_root.parent
    target = (
        milestones_root
        / "project-milestone-3-group-2"
        / "scripts"
        / "export_m3_deploy_headers.py"
    )
    if not target.is_file():
        print(f"error: exporter not found: {target}", file=sys.stderr)
        return 2

    argv = sys.argv[1:]
    has_har = any(a == "--har-mcu" or a.startswith("--har-mcu=") for a in argv)
    cmd = [sys.executable, str(target)]
    if not has_har:
        cmd.extend(["--har-mcu", str(har_root)])
    cmd.extend(argv)

    env = dict(os.environ)
    return subprocess.call(cmd, env=env)


if __name__ == "__main__":
    raise SystemExit(main())
