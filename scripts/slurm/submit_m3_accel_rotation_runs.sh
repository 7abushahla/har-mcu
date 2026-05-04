#!/usr/bin/env bash
set -euo pipefail

# Submit one sequential Slurm job for the M3 accelerometer-rotation reruns.
# Outputs are isolated under:
#   models_tflite/m3/<experiment_id>/accel_rotation/<model_variant>/<experiment_code>/

if [ -f symbolic-motifgen/scripts/aus_hpc_env.sh ]; then
  source symbolic-motifgen/scripts/aus_hpc_env.sh
elif [ -f ../symbolic-motifgen/scripts/aus_hpc_env.sh ]; then
  source ../symbolic-motifgen/scripts/aus_hpc_env.sh
fi

REPO_ROOT="${M3_REPO_ROOT:-/shared/b00088568/github/har-mcu}"
CONDA_ENV="${M3_CONDA_ENV:-/shared/b00088568/myenvs/tinymlproj}"
ACCOUNT="${M3_SLURM_ACCOUNT:-acc-izualkernan}"
QOS="${M3_SLURM_QOS:-gpu-medium-izualkernan-001}"
PARTITION="${M3_SLURM_PARTITION:-gpu}"
GRES="${M3_SLURM_GRES:-gpu:1}"
CPUS="${M3_SLURM_CPUS:-4}"
MEM="${M3_SLURM_MEM:-15G}"
TIME_LIMIT="${M3_SLURM_TIME:-96:00:00}"
MAX_ACTIVE_JOBS="${M3_MAX_ACTIVE_JOBS:-15}"
EXCLUDE="${M3_SLURM_EXCLUDE:-}"

SBATCH_GRES_LINE=""
if [ -n "$GRES" ]; then
  SBATCH_GRES_LINE="#SBATCH --gres=${GRES}"
fi
SBATCH_EXCLUDE_LINE=""
if [ -n "$EXCLUDE" ]; then
  SBATCH_EXCLUDE_LINE="#SBATCH --exclude=${EXCLUDE}"
fi

ACTIVE_JOBS="$(squeue -u "$USER" -h 2>/dev/null | wc -l | sed 's/[[:space:]]//g')"
if [ "${ACTIVE_JOBS:-0}" -ge "$MAX_ACTIVE_JOBS" ]; then
  echo "Refusing to submit: active jobs (${ACTIVE_JOBS}) >= cap (${MAX_ACTIVE_JOBS})." >&2
  exit 1
fi

mkdir -p "$REPO_ROOT/slurm_logs"

sbatch <<SBATCH
#!/usr/bin/env bash
#SBATCH --job-name=m3_accelrot_dc_daghero
#SBATCH --account=${ACCOUNT}
#SBATCH --qos=${QOS}
#SBATCH --partition=${PARTITION}
${SBATCH_GRES_LINE}
#SBATCH --cpus-per-task=${CPUS}
#SBATCH --mem=${MEM}
#SBATCH --time=${TIME_LIMIT}
${SBATCH_EXCLUDE_LINE}
#SBATCH --output=${REPO_ROOT}/slurm_logs/%x.%j.out
#SBATCH --error=${REPO_ROOT}/slurm_logs/%x.%j.err

set -euo pipefail

cd "${REPO_ROOT}"
source ~/.bashrc >/dev/null 2>&1 || true
if command -v conda >/dev/null 2>&1; then
  CONDA_BASE="\$(conda info --base 2>/dev/null || true)"
  if [ -n "\${CONDA_BASE}" ] && [ -f "\${CONDA_BASE}/etc/profile.d/conda.sh" ]; then
    source "\${CONDA_BASE}/etc/profile.d/conda.sh"
  fi
fi
if command -v conda >/dev/null 2>&1; then
  set +e
  conda activate "${CONDA_ENV}"
  CONDA_STATUS=\$?
  set -e
  if [ "\${CONDA_STATUS}" -ne 0 ]; then
    export PATH="${CONDA_ENV}/bin:\${PATH}"
  fi
else
  export PATH="${CONDA_ENV}/bin:\${PATH}"
fi

ENV_PY="${CONDA_ENV}/bin/python"
if [ ! -x "\$ENV_PY" ]; then
  ENV_PY="\$(command -v python)"
fi

declare -a JOBS=(
  "configs/m3/E00_wisdm_m2_anchor.yaml"
  "configs/m3/E03_arduino_downsample_20hz_T100.yaml"
  "configs/m3/E04_wisdm_to_g_arduino_g.yaml"
  "configs/m3/E05_legacy_arduino_to_mps2.yaml"
  "configs/m3/E06_no_norm_matched.yaml"
  "configs/m3/E07_skip_inference_norm_diag.yaml"
  "configs/m3/E08_T50_window.yaml"
  "configs/m3/E09_wisdm_pretrain_arduino_finetune.yaml"
  "configs/m3/E10_arduino_from_scratch.yaml"
  "configs/m3/E11_wisdm_pretrain_arduino_finetune_T50.yaml"
  "configs/m3/E12_arduino_from_scratch_T50.yaml"
)

for cfg in "\${JOBS[@]}"; do
  echo "========== M3 accel rotation DeepConvLSTM: \$cfg =========="
  "\$ENV_PY" -u -m src.m3.run_experiment \\
    --config "\$cfg" \\
    --artifact-suffix "accel_rotation/deepconv_lstm_conv2d/{experiment_code}" \\
    --full-dataset
done

for cfg in "\${JOBS[@]}"; do
  echo "========== M3 accel rotation Daghero: \$cfg =========="
  "\$ENV_PY" -u -m src.m3.run_experiment \\
    --config "\$cfg" \\
    --model-variant daghero_cnn_2layer_conv2d \\
    --artifact-suffix "accel_rotation/daghero_cnn_2layer_conv2d/{experiment_code}" \\
    --full-dataset
done

echo "Done M3 accelerometer-rotation reruns for DeepConvLSTM and Daghero (\${#JOBS[@]} configs each)."
SBATCH
