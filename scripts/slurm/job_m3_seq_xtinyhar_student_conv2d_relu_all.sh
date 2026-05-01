#!/bin/bash
#SBATCH --account=acc-mialhajri
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=24G
#SBATCH --time=500:00:00
#SBATCH --job-name=m3-seq-xthrelu
#
# One GPU: nine M3 experiments with xtinyhar_student_conv2d_relu (TFLM-friendly; sequential).
# E08 uses patch_size=10 (T50) per runbook.
#   sbatch scripts/slurm/job_m3_seq_xtinyhar_student_conv2d_relu_all.sh
# Each run uses --full-dataset (full windowed data).
#

set -e

MODEL_VARIANT="xtinyhar_student_conv2d_relu"

ENV_PATH="/shared/b00090279/tinymlproj"
source /opt/miniconda/etc/profile.d/conda.sh
conda activate "$ENV_PATH"
[[ "$CONDA_PREFIX" == "$ENV_PATH" ]] || { echo "[NO] conda"; exit 1; }

if [[ -n "${SLURM_SUBMIT_DIR:-}" ]]; then cd "$SLURM_SUBMIT_DIR"
else cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; fi
ENV_PY="$CONDA_PREFIX/bin/python"

declare -a JOBS=(
  "configs/m3/E00_wisdm_m2_anchor.yaml|full_e00"
  "configs/m3/E03_arduino_downsample_20hz_T100.yaml|full_e03"
  "configs/m3/E04_wisdm_to_g_arduino_g.yaml|full_e04"
  "configs/m3/E05_legacy_arduino_to_mps2.yaml|full_e05"
  "configs/m3/E06_no_norm_matched.yaml|full_e06"
  "configs/m3/E07_skip_inference_norm_diag.yaml|full_e07"
  "configs/m3/E08_T50_window.yaml|full_e08"
  "configs/m3/E09_wisdm_pretrain_arduino_finetune.yaml|full_e09"
  "configs/m3/E10_arduino_from_scratch.yaml|full_e10"
)

for item in "${JOBS[@]}"; do
  IFS='|' read -r cfg _suf <<<"$item"
  echo "========== M3 sequential ${MODEL_VARIANT}: $cfg =========="
  extra=()
  if [[ "$cfg" == *E08_* ]]; then
    extra=( --model-kwarg patch_size=10 )
  fi
  "$ENV_PY" -u -m src.m3.run_experiment \
    --config "$cfg" \
    --model-variant "$MODEL_VARIANT" \
    --artifact-suffix "arch_seq/{model_variant}/{experiment_code}" \
    "${extra[@]}" \
    --full-dataset
done

echo "Done M3 sequential ${MODEL_VARIANT} (9 runs)."
