#!/bin/bash
#SBATCH --account=acc-mialhajri
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=500:00:00
#SBATCH --job-name=m3-e11-t50-all
#
# One GPU job: E11 (WISDM pretrain + Arduino fine-tune @ T=50) for all seven model variants, back-to-back.
# Compare outputs to E09 @ T=100 (full_e09 or arch_seq/<variant>/e09).
# Artifacts: arch_seq/<model_variant>/e11/...
#
# From har-mcu repo root:
#   sbatch scripts/slurm/job_m3_seq_e11_t50_all_models.sh
#

set -e

ENV_PATH="/shared/b00090279/tinymlproj"
source /opt/miniconda/etc/profile.d/conda.sh
conda activate "$ENV_PATH"
[[ "$CONDA_PREFIX" == "$ENV_PATH" ]] || { echo "[NO] conda"; exit 1; }

if [[ -n "${SLURM_SUBMIT_DIR:-}" ]]; then cd "$SLURM_SUBMIT_DIR"
else cd "$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; fi
ENV_PY="$CONDA_PREFIX/bin/python"

CFG="configs/m3/E11_wisdm_pretrain_arduino_finetune_T50.yaml"

declare -a MODEL_VARIANTS=(
  deepconv_lstm_conv2d
  daghero_cnn_2layer_conv2d
  repmobile_folded_conv2d
  tcn_attention_har_teacher_conv2d
  tcn_inception_conv2d
  xtinyhar_student_conv2d
  xtinyhar_student_conv2d_relu
)

for mv in "${MODEL_VARIANTS[@]}"; do
  echo "========== E11 T=50: $mv =========="
  extra=()
  if [[ "$mv" == xtinyhar_student_conv2d ]] || [[ "$mv" == xtinyhar_student_conv2d_relu ]]; then
    extra=( --model-kwarg patch_size=10 )
  fi
  "$ENV_PY" -u -m src.m3.run_experiment \
    --config "$CFG" \
    --model-variant "$mv" \
    --artifact-suffix "arch_seq/{model_variant}/{experiment_code}" \
    "${extra[@]}" \
    --full-dataset
done

echo "Done E11 T=50 (all ${#MODEL_VARIANTS[@]} models)."
