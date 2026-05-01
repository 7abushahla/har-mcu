#!/bin/bash
#SBATCH --account=acc-mialhajri
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=15G
#SBATCH --time=48:00:00
#SBATCH --job-name=har-m3-exp
#
# har-mcu Milestone 3: one full run (FP32 / PTQ / QAT as in YAML).
# Submit from the har-mcu repo root, e.g.:
#   export M3_CONFIG=configs/m3/E00_wisdm_m2_anchor.yaml
#   export M3_EXTRA_ARGS="--artifact-suffix full_e00"
#   sbatch scripts/slurm/job_m3_experiment.sh
#
# Edit ENV_PATH below if your tinymlproj prefix differs.
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

: "${M3_CONFIG:?Set M3_CONFIG, e.g. configs/m3/E00_wisdm_m2_anchor.yaml}"

"$ENV_PY" -u -m src.m3.run_experiment --config "$M3_CONFIG" ${M3_EXTRA_ARGS:-}

echo "Done har-m3."
