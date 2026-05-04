#!/usr/bin/env bash
set -euo pipefail

# Submit full-dataset training for the M3 v3 target-orientation rotation run.
# V3 trains only the augmentation-on artifacts and reuses the clean
# no-augmentation v2 baseline for dual-domain off/on evaluation.
#
# Default v3 policy:
#   augment.accel_rotation.mode=target_gravity
#   augment.accel_rotation.probability=0.25
#   augment.accel_rotation.target_vectors=[-x, -y, +z]
#   augment.accel_rotation.target_probabilities=[0.50, 0.25, 0.25]

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
TIME_LIMIT="${M3_ROT_V3_SLURM_TIME:-${M3_SLURM_TIME:-96:00:00}}"
MAX_ACTIVE_JOBS="${M3_MAX_ACTIVE_JOBS:-15}"
ARRAY_CONCURRENCY="${M3_ROT_V3_ARRAY_CONCURRENCY:-2}"
EXCLUDE="${M3_SLURM_EXCLUDE:-gpu-dy-g5-0-83,gpu-dy-g5-0-88}"

V3_PROBABILITY="${M3_ROT_V3_PROBABILITY:-0.25}"
V3_TARGET_VECTORS="${M3_ROT_V3_TARGET_VECTORS:--1,0,0;0,-1,0;0,0,1}"
V3_TARGET_PROBABILITIES="${M3_ROT_V3_TARGET_PROBABILITIES:-0.50,0.25,0.25}"
V3_SUFFIX_ROOT="${M3_ROT_V3_SUFFIX_ROOT:-accel_rotation_v3_target_clusters_p025}"

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
  --job-name=m3_rot_v3_train \
  --account="$ACCOUNT" \
  --qos="$QOS" \
  --partition="$PARTITION" \
  "${SBATCH_GRES_ARGS[@]}" \
  --cpus-per-task="$CPUS" \
  --mem="$MEM" \
  --time="$TIME_LIMIT" \
  "${SBATCH_EXCLUDE_ARGS[@]}" \
  --array="0-1%${ARRAY_CONCURRENCY}" \
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

declare -a CONFIGS=(
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

case "\$SLURM_ARRAY_TASK_ID" in
  0)
    model="deepconv_lstm_conv2d"
    ;;
  1)
    model="daghero_cnn_2layer_conv2d"
    ;;
  *)
    echo "Unknown SLURM_ARRAY_TASK_ID=\$SLURM_ARRAY_TASK_ID" >&2
    exit 2
    ;;
esac

for cfg in "\${CONFIGS[@]}"; do
  echo "========== M3 rotation v3 target_gravity model=\$model cfg=\$cfg =========="
  args=(
    -m src.m3.run_experiment
    --config "\$cfg"
    --artifact-suffix "${V3_SUFFIX_ROOT}/{model_variant}/{experiment_code}"
    --full-dataset
    --enable-accel-rotation
    --accel-rotation-mode target_gravity
    --accel-rotation-probability "${V3_PROBABILITY}"
    --accel-rotation-target-vectors="${V3_TARGET_VECTORS}"
    --accel-rotation-target-probabilities "${V3_TARGET_PROBABILITIES}"
  )
  if [ "\$model" != "deepconv_lstm_conv2d" ]; then
    args+=(--model-variant "\$model")
  fi
  "\$ENV_PY" -u "\${args[@]}"
done

echo "Done M3 rotation v3 target_gravity model=\$model configs=\${#CONFIGS[@]}"
SBATCH
