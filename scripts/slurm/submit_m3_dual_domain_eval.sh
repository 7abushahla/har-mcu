#!/usr/bin/env bash
set -euo pipefail

# Submit an eval-only Slurm array for the M3 augmentation off/on comparison.
# Each array task evaluates one (config, model_variant, augment_label) artifact
# bundle on both WISDM and Arduino test splits for FP32/PTQ/QAT TFLite.

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
GRES="${M3_DUAL_EVAL_SLURM_GRES:-${M3_SLURM_GRES:-gpu:1}}"
CPUS="${M3_DUAL_EVAL_SLURM_CPUS:-${M3_SLURM_CPUS:-4}}"
MEM="${M3_DUAL_EVAL_SLURM_MEM:-${M3_SLURM_MEM:-12G}}"
TIME_LIMIT="${M3_DUAL_EVAL_SLURM_TIME:-${M3_SLURM_TIME:-08:00:00}}"
MAX_ACTIVE_JOBS="${M3_MAX_ACTIVE_JOBS:-15}"
ARRAY_CONCURRENCY="${M3_DUAL_EVAL_ARRAY_CONCURRENCY:-12}"
TASK_START="${M3_DUAL_EVAL_TASK_START:-0}"
TASK_LIMIT="${M3_DUAL_EVAL_TASK_LIMIT:-15}"
TASKS_PER_ARRAY_TASK="${M3_DUAL_EVAL_TASKS_PER_ARRAY_TASK:-${M3_DUAL_EVAL_TASKS_PER_ARRAY:-1}}"
MATRIX_ONLY="${M3_DUAL_EVAL_MATRIX_ONLY:-0}"
DEPENDENCY="${M3_SLURM_DEPENDENCY:-}"
OUTPUT_DIR="${M3_DUAL_EVAL_OUTPUT_DIR:-reports/m3/dual_domain_eval}"
if [ -n "${M3_DUAL_EVAL_ON_ARTIFACT_SUFFIX:-}" ]; then
  ON_ARTIFACT_SUFFIX="$M3_DUAL_EVAL_ON_ARTIFACT_SUFFIX"
else
  ON_ARTIFACT_SUFFIX='accel_rotation/{model_variant}/{experiment_code}'
fi
if [ -n "${M3_DUAL_EVAL_OFF_ARTIFACT_SUFFIX:-}" ]; then
  OFF_ARTIFACT_SUFFIX="$M3_DUAL_EVAL_OFF_ARTIFACT_SUFFIX"
else
  OFF_ARTIFACT_SUFFIX='no_accel_rotation/{model_variant}/{experiment_code}'
fi
EXCLUDE="${M3_SLURM_EXCLUDE:-gpu-dy-g5-0-83,gpu-dy-g5-0-88}"

SBATCH_GRES_ARGS=()
if [ -n "$GRES" ]; then
  SBATCH_GRES_ARGS=(--gres="$GRES")
fi
SBATCH_EXCLUDE_ARGS=()
if [ -n "$EXCLUDE" ]; then
  SBATCH_EXCLUDE_ARGS=(--exclude="$EXCLUDE")
fi
SBATCH_DEPENDENCY_ARGS=()
if [ -n "$DEPENDENCY" ]; then
  SBATCH_DEPENDENCY_ARGS=(--dependency="$DEPENDENCY")
fi

ACTIVE_JOBS="$(squeue -u "$USER" -h 2>/dev/null | wc -l | sed 's/[[:space:]]//g')"
if [ "${ACTIVE_JOBS:-0}" -ge "$MAX_ACTIVE_JOBS" ]; then
  echo "Refusing to submit: active jobs (${ACTIVE_JOBS}) >= cap (${MAX_ACTIVE_JOBS})." >&2
  exit 1
fi

mkdir -p "$REPO_ROOT/slurm_logs" "$REPO_ROOT/$OUTPUT_DIR"
JOB_FILE="$REPO_ROOT/$OUTPUT_DIR/job_matrix.tsv"
: > "$JOB_FILE"

declare -a CONFIGS=(
  "configs/m3/E00_wisdm_m2_anchor.yaml|E00"
  "configs/m3/E03_arduino_downsample_20hz_T100.yaml|E03"
  "configs/m3/E04_wisdm_to_g_arduino_g.yaml|E04"
  "configs/m3/E05_legacy_arduino_to_mps2.yaml|E05"
  "configs/m3/E06_no_norm_matched.yaml|E06"
  "configs/m3/E07_skip_inference_norm_diag.yaml|E07"
  "configs/m3/E08_T50_window.yaml|E08"
  "configs/m3/E09_wisdm_pretrain_arduino_finetune.yaml|E09"
  "configs/m3/E10_arduino_from_scratch.yaml|E10"
  "configs/m3/E11_wisdm_pretrain_arduino_finetune_T50.yaml|E11"
  "configs/m3/E12_arduino_from_scratch_T50.yaml|E12"
)

declare -a MODELS=(
  "deepconv_lstm_conv2d"
  "daghero_cnn_2layer_conv2d"
)

for item in "${CONFIGS[@]}"; do
  IFS='|' read -r cfg code <<<"$item"
  code_lower="${code,,}"
  for model in "${MODELS[@]}"; do
    # Augmentation ON artifacts.
    printf '%s\t%s\t%s\t%s\t%s\n' \
      "$cfg" "$model" "on" "$ON_ARTIFACT_SUFFIX" "" >> "$JOB_FILE"

    # Augmentation OFF artifacts from the clean no-rotation rerun.
    off_suffix="$OFF_ARTIFACT_SUFFIX"
    off_run_id=""
    printf '%s\t%s\t%s\t%s\t%s\n' \
      "$cfg" "$model" "off" "$off_suffix" "$off_run_id" >> "$JOB_FILE"
  done
done

TASK_COUNT="$(wc -l < "$JOB_FILE" | sed 's/[[:space:]]//g')"
if [ "${TASK_COUNT:-0}" -le 0 ]; then
  echo "No jobs generated." >&2
  exit 1
fi
if [ "${MATRIX_ONLY}" = "1" ]; then
  echo "Generated ${TASK_COUNT} dual-domain eval tasks."
  echo "Job matrix: ${JOB_FILE}"
  exit 0
fi
if [ "${TASK_START}" -lt 0 ] || [ "${TASK_START}" -ge "${TASK_COUNT}" ]; then
  echo "Invalid M3_DUAL_EVAL_TASK_START=${TASK_START}; task count is ${TASK_COUNT}." >&2
  exit 1
fi
if [ "${TASK_LIMIT}" -le 0 ]; then
  echo "Invalid M3_DUAL_EVAL_TASK_LIMIT=${TASK_LIMIT}; expected a positive integer." >&2
  exit 1
fi
if [ "${TASKS_PER_ARRAY_TASK}" -le 0 ]; then
  echo "Invalid M3_DUAL_EVAL_TASKS_PER_ARRAY_TASK=${TASKS_PER_ARRAY_TASK}; expected a positive integer." >&2
  exit 1
fi
ROW_END=$((TASK_START + TASK_LIMIT - 1))
if [ "${ROW_END}" -ge "${TASK_COUNT}" ]; then
  ROW_END=$((TASK_COUNT - 1))
fi
ROW_COUNT=$((ROW_END - TASK_START + 1))
ARRAY_SIZE=$(((ROW_COUNT + TASKS_PER_ARRAY_TASK - 1) / TASKS_PER_ARRAY_TASK))
ARRAY_MAX=$((ARRAY_SIZE - 1))
if [ "${ARRAY_CONCURRENCY}" -gt "${ARRAY_SIZE}" ]; then
  ARRAY_CONCURRENCY="${ARRAY_SIZE}"
fi

sbatch \
  --job-name=m3_dual_eval \
  --account="$ACCOUNT" \
  --qos="$QOS" \
  --partition="$PARTITION" \
  "${SBATCH_GRES_ARGS[@]}" \
  --cpus-per-task="$CPUS" \
  --mem="$MEM" \
  --time="$TIME_LIMIT" \
  "${SBATCH_EXCLUDE_ARGS[@]}" \
  "${SBATCH_DEPENDENCY_ARGS[@]}" \
  --array="0-${ARRAY_MAX}%${ARRAY_CONCURRENCY}" \
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

first_row=\$(( ${TASK_START} + SLURM_ARRAY_TASK_ID * ${TASKS_PER_ARRAY_TASK} ))
last_row=\$(( first_row + ${TASKS_PER_ARRAY_TASK} - 1 ))
if [ "\$last_row" -gt "${ROW_END}" ]; then
  last_row="${ROW_END}"
fi

for matrix_row in \$(seq "\$first_row" "\$last_row"); do
  line="\$(sed -n "\$((matrix_row + 1))p" "${JOB_FILE}")"
  IFS=\$'\t' read -r cfg model augment_label artifact_suffix run_id <<<"\$line"

  echo "matrix_row=\$matrix_row"
  echo "config=\$cfg"
  echo "model=\$model"
  echo "augment_label=\$augment_label"
  echo "artifact_suffix=\$artifact_suffix"
  echo "run_id=\$run_id"

  args=(
    -m src.m3.dual_domain_eval
    --config "\$cfg"
    --model-variant "\$model"
    --augment-label "\$augment_label"
    --artifact-suffix "\$artifact_suffix"
    --output-dir "${OUTPUT_DIR}"
  )
  if [ -n "\$run_id" ]; then
    args+=(--run-id "\$run_id")
  fi

  "\$ENV_PY" "\${args[@]}"
done
SBATCH

echo "Submitted ${ROW_COUNT}/${TASK_COUNT} dual-domain eval matrix rows (${TASK_START}-${ROW_END}) as ${ARRAY_SIZE} Slurm tasks with concurrency ${ARRAY_CONCURRENCY}."
echo "Job matrix: ${JOB_FILE}"
if [ "${ROW_END}" -lt $((TASK_COUNT - 1)) ]; then
  echo "Submit the next chunk with:"
  echo "  M3_DUAL_EVAL_TASK_START=$((ROW_END + 1)) M3_DUAL_EVAL_TASK_LIMIT=${TASK_LIMIT} bash scripts/slurm/submit_m3_dual_domain_eval.sh"
fi
echo "After completion, aggregate with:"
echo "  ${CONDA_ENV}/bin/python -m src.m3.dual_domain_eval --aggregate-only --output-dir ${OUTPUT_DIR}"
