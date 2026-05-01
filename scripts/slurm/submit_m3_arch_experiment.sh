#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
  echo "Usage: bash scripts/slurm/submit_m3_arch_experiment.sh configs/m3/E00_wisdm_m2_anchor.yaml <model_variant> [runner args]" >&2
  echo "Example: bash scripts/slurm/submit_m3_arch_experiment.sh configs/m3/E00_wisdm_m2_anchor.yaml daghero_cnn_2layer_conv2d --smoke" >&2
  exit 2
fi

CONFIG="$1"
MODEL_VARIANT="$2"
shift 2 || true

JOB_BASENAME="$(basename "$CONFIG" .yaml)"
EXPERIMENT_CODE="${JOB_BASENAME%%_*}"
EXPERIMENT_CODE="${EXPERIMENT_CODE,,}"
DEFAULT_SUFFIX="arch_sweeps/${MODEL_VARIANT}/${EXPERIMENT_CODE}"

HAS_SUFFIX=0
for arg in "$@"; do
  if [ "$arg" = "--artifact-suffix" ] || [[ "$arg" == --artifact-suffix=* ]]; then
    HAS_SUFFIX=1
  fi
done

CMD=(
  bash scripts/slurm/submit_m3_experiment.sh
  "$CONFIG"
  --model-variant "$MODEL_VARIANT"
)

if [ "$HAS_SUFFIX" -eq 0 ]; then
  CMD+=(--artifact-suffix "${M3_ARTIFACT_SUFFIX:-$DEFAULT_SUFFIX}")
fi

CMD+=("$@")

printf '%q ' "${CMD[@]}"
printf '\n'
"${CMD[@]}"
