#!/usr/bin/env bash
set -euo pipefail

# Submit the dual-domain eval matrix for the v3 target-orientation run.
# Pass M3_SLURM_DEPENDENCY=afterok:<TRAIN_JOBID> when submitting after training.
# The off baseline intentionally reuses the clean no-augmentation v2 artifacts.

export M3_DUAL_EVAL_OUTPUT_DIR="${M3_DUAL_EVAL_OUTPUT_DIR:-reports/m3/dual_domain_eval_v3_target_clusters_p025}"
if [ -z "${M3_DUAL_EVAL_ON_ARTIFACT_SUFFIX:-}" ]; then
  export M3_DUAL_EVAL_ON_ARTIFACT_SUFFIX='accel_rotation_v3_target_clusters_p025/{model_variant}/{experiment_code}'
fi
if [ -z "${M3_DUAL_EVAL_OFF_ARTIFACT_SUFFIX:-}" ]; then
  export M3_DUAL_EVAL_OFF_ARTIFACT_SUFFIX='no_accel_rotation_v2/{model_variant}/{experiment_code}'
fi
export M3_DUAL_EVAL_TASK_START="${M3_DUAL_EVAL_TASK_START:-0}"
export M3_DUAL_EVAL_TASK_LIMIT="${M3_DUAL_EVAL_TASK_LIMIT:-44}"
export M3_DUAL_EVAL_TASKS_PER_ARRAY_TASK="${M3_DUAL_EVAL_TASKS_PER_ARRAY_TASK:-4}"
export M3_DUAL_EVAL_ARRAY_CONCURRENCY="${M3_DUAL_EVAL_ARRAY_CONCURRENCY:-11}"

bash scripts/slurm/submit_m3_dual_domain_eval.sh
