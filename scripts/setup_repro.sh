#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf '%s\n' \
    "Usage: bash scripts/setup_repro.sh [--env-name NAME] [--skip-env] [--yes] [setup_repro.py args...]" \
    "" \
    "By default, creates/updates conda and downloads/validates WISDM plus Arduino data." \
    "Common local run:" \
    "  bash scripts/setup_repro.sh --yes" \
    "" \
    "Use the current active environment and only prepare data:" \
    "  bash scripts/setup_repro.sh --skip-env" \
    "" \
    "Run local smoke checks after setup:" \
    "  bash scripts/setup_repro.sh --notebook-check smoke --m3-check smoke --v2-augment-check smoke"
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
ENV_NAME="${HAR_MCU_ENV_NAME:-tinymlproj}"
SKIP_ENV=0
YES=0
PY_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --env-name)
      ENV_NAME="$2"
      shift 2
      ;;
    --skip-env)
      SKIP_ENV=1
      shift
      ;;
    --yes|-y)
      YES=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      PY_ARGS+=("$1")
      shift
      ;;
  esac
done

cd "$REPO_ROOT"

if [[ "$SKIP_ENV" -eq 1 ]]; then
  python scripts/setup_repro.py "${PY_ARGS[@]}"
  exit 0
fi

if ! command -v conda >/dev/null 2>&1; then
  printf '%s\n' "conda was not found on PATH. Install conda or rerun with --skip-env in an active environment." >&2
  exit 1
fi

CONDA_YES_ARGS=()
if [[ "$YES" -eq 1 ]]; then
  CONDA_YES_ARGS=(-y)
fi

if conda env list | awk '{print $1}' | grep -qx "$ENV_NAME"; then
  printf '%s\n' "[setup] updating conda env: $ENV_NAME"
  conda env update -n "$ENV_NAME" -f environment.yml --prune
else
  printf '%s\n' "[setup] creating conda env: $ENV_NAME"
  conda env create -n "$ENV_NAME" -f environment.yml "${CONDA_YES_ARGS[@]}"
fi

conda run -n "$ENV_NAME" python scripts/setup_repro.py "${PY_ARGS[@]}"
