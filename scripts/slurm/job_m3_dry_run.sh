#!/bin/bash
#SBATCH --account=acc-mialhajri
#SBATCH --partition=cpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=00:15:00
#SBATCH --job-name=har-m3-dry
#
# Config validation only (no training). Submit from har-mcu repo root:
#   export M3_CONFIG=configs/m3/E00_wisdm_m2_anchor.yaml
#   sbatch scripts/slurm/job_m3_dry_run.sh
#

set -e

ENV_PATH="/shared/b00090279/tinymlproj"
source /opt/miniconda/etc/profile.d/conda.sh
conda activate "$ENV_PATH"
[[ "$CONDA_PREFIX" == "$ENV_PATH" ]] || { echo "[NO] conda"; exit 1; }

if [[ -n "${SLURM_SUBMIT_DIR:-}" ]]; then cd "$SLURM_SUBMIT_DIR"
else cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; fi
REPO_ROOT="$(pwd)"
ENV_PY="$CONDA_PREFIX/bin/python"

cd "$REPO_ROOT"

: "${M3_CONFIG:?Set M3_CONFIG}"

"$ENV_PY" -u -m src.m3.run_experiment --config "$M3_CONFIG" --dry-run

echo "Done har-m3 dry-run."
