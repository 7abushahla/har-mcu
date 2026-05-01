#!/usr/bin/env bash
# Submit nine full DeepConvLSTM M3 jobs (E00 + E03–E10), same style as job_m3_experiment.sh.
#
# Usage (login node): run from har-mcu repo root so SLURM_SUBMIT_DIR matches (same as QCFS+ jobs).
#   cd /shared/b00090279/TinyML-Course/har-mcu
#   bash scripts/slurm/submit_m3_matrix_e00_e10.sh
#
# Conda: edit ENV_PATH in scripts/slurm/job_m3_experiment.sh if needed.
#
# Prerequisites: same #SBATCH account/partition as in job_m3_experiment.sh (edit that file if needed).

set -euo pipefail

REPO="${HARMCU_REPO_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"

cd "$REPO"
JOB_SCRIPT="$REPO/scripts/slurm/job_m3_experiment.sh"
[[ -f "$JOB_SCRIPT" ]] || { echo "missing $JOB_SCRIPT"; exit 1; }

declare -a PAIRS=(
  "configs/m3/E00_wisdm_m2_anchor.yaml:full_e00"
  "configs/m3/E03_arduino_downsample_20hz_T100.yaml:full_e03"
  "configs/m3/E04_wisdm_to_g_arduino_g.yaml:full_e04"
  "configs/m3/E05_legacy_arduino_to_mps2.yaml:full_e05"
  "configs/m3/E06_no_norm_matched.yaml:full_e06"
  "configs/m3/E07_skip_inference_norm_diag.yaml:full_e07"
  "configs/m3/E08_T50_window.yaml:full_e08"
  "configs/m3/E09_wisdm_pretrain_arduino_finetune.yaml:full_e09"
  "configs/m3/E10_arduino_from_scratch.yaml:full_e10"
)

for entry in "${PAIRS[@]}"; do
  IFS=: read -r cfg suffix <<<"$entry"
  export M3_CONFIG="$cfg"
  export M3_EXTRA_ARGS="--artifact-suffix $suffix"
  echo "sbatch -J m3_${suffix} $M3_CONFIG $M3_EXTRA_ARGS"
  sbatch -J "m3_${suffix}" "$JOB_SCRIPT"
done

echo "Submitted ${#PAIRS[@]} jobs. Monitor: squeue -u \$USER"
