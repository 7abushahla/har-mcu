#!/usr/bin/env bash
set -euo pipefail

# Submit full-dataset training for the M3 v2 rotation ablation:
#   no augmentation v2 baseline vs bounded SO(3) v2 augmentation,
#   for DeepConvLSTM and Daghero.
#
# Default v2 policy:
#   augment.accel_rotation.mode=bounded_so3
#   augment.accel_rotation.probability=0.25
#   augment.accel_rotation.max_angle_degrees=20

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
TIME_LIMIT="${M3_ROT_V2_SLURM_TIME:-${M3_SLURM_TIME:-96:00:00}}"
MAX_ACTIVE_JOBS="${M3_MAX_ACTIVE_JOBS:-15}"
ARRAY_CONCURRENCY="${M3_ROT_V2_ARRAY_CONCURRENCY:-4}"
EXCLUDE="${M3_SLURM_EXCLUDE:-gpu-dy-g5-0-83,gpu-dy-g5-0-88}"

V2_MODE="${M3_ROT_V2_MODE:-bounded_so3}"
V2_PROBABILITY="${M3_ROT_V2_PROBABILITY:-0.25}"
V2_MAX_ANGLE_DEGREES="${M3_ROT_V2_MAX_ANGLE_DEGREES:-20}"
V2_SUFFIX_ROOT="${M3_ROT_V2_SUFFIX_ROOT:-accel_rotation_v2_bounded20_p025}"
V2_OFF_SUFFIX_ROOT="${M3_ROT_V2_OFF_SUFFIX_ROOT:-no_accel_rotation_v2}"
V2_CONFIGS_CSV="${M3_ROT_V2_CONFIGS:-}"

SBATCH_GRES_ARGS=()
if [ -n "$GRES" ]; then
  SBATCH_GRES_ARGS=(--gres="$GRES")
fi
SBATCH_EXCLUDE_ARGS=()
if [ -n "$EXCLUDE" ]; then
  SBATCH_EXCLUDE_ARGS=(--exclude="$EXCLUDE")
fi

ACTIVE_JOBS="$(squeue -u "$USER" -h 2>/dev/null | wc -l | sed 's/[[:space:]]//g')"
if [ "${ACTIVE_JOBS:-0}" -ge "$MAX_ACTIVE_JOBS" ]; then
  echo "Refusing to submit: active jobs (${ACTIVE_JOBS}) >= cap (${MAX_ACTIVE_JOBS})." >&2
  exit 1
fi

mkdir -p "$REPO_ROOT/slurm_logs"

sbatch \
  --job-name=m3_rot_v2_train \
  --account="$ACCOUNT" \
  --qos="$QOS" \
  --partition="$PARTITION" \
  "${SBATCH_GRES_ARGS[@]}" \
  --cpus-per-task="$CPUS" \
  --mem="$MEM" \
  --time="$TIME_LIMIT" \
  "${SBATCH_EXCLUDE_ARGS[@]}" \
  --array="0-3%${ARRAY_CONCURRENCY}" \
  --output="$REPO_ROOT/slurm_logs/%x.%A_%a.out" \
  --error="$REPO_ROOT/slurm_logs/%x.%A_%a.err" <<SBATCH
#!/usr/bin/env bash
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

declare -a DEFAULT_CONFIGS=(
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

declare -a CONFIGS=()
if [ -n "${V2_CONFIGS_CSV}" ]; then
  IFS=',' read -r -a CONFIGS <<< "${V2_CONFIGS_CSV}"
else
  CONFIGS=("${DEFAULT_CONFIGS[@]}")
fi

case "\$SLURM_ARRAY_TASK_ID" in
  0)
    condition="off"
    suffix_root="${V2_OFF_SUFFIX_ROOT}"
    model="deepconv_lstm_conv2d"
    ;;
  1)
    condition="off"
    suffix_root="${V2_OFF_SUFFIX_ROOT}"
    model="daghero_cnn_2layer_conv2d"
    ;;
  2)
    condition="on"
    suffix_root="${V2_SUFFIX_ROOT}"
    model="deepconv_lstm_conv2d"
    ;;
  3)
    condition="on"
    suffix_root="${V2_SUFFIX_ROOT}"
    model="daghero_cnn_2layer_conv2d"
    ;;
  *)
    echo "Unknown SLURM_ARRAY_TASK_ID=\$SLURM_ARRAY_TASK_ID" >&2
    exit 2
    ;;
esac

for cfg in "\${CONFIGS[@]}"; do
  echo "========== M3 rotation v2 condition=\$condition model=\$model cfg=\$cfg =========="
  args=(
    -m src.m3.run_experiment
    --config "\$cfg"
    --artifact-suffix "\${suffix_root}/{model_variant}/{experiment_code}"
    --full-dataset
  )
  if [ "\$model" != "deepconv_lstm_conv2d" ]; then
    args+=(--model-variant "\$model")
  fi
  if [ "\$condition" = "off" ]; then
    args+=(--disable-accel-rotation)
  else
    args+=(
      --enable-accel-rotation
      --accel-rotation-mode "${V2_MODE}"
      --accel-rotation-probability "${V2_PROBABILITY}"
      --accel-rotation-max-angle-degrees "${V2_MAX_ANGLE_DEGREES}"
    )
  fi
  "\$ENV_PY" -u "\${args[@]}"
done

echo "Done M3 rotation v2 condition=\$condition model=\$model configs=\${#CONFIGS[@]}"
SBATCH
