#!/usr/bin/env bash
set -euo pipefail

# Keep the M3 dual-domain eval matrix moving under the QOS submitted-job cap.
# This script submits chunks only when `squeue` shows enough headroom.

REPO_ROOT="${M3_REPO_ROOT:-/shared/b00088568/github/har-mcu}"
SUBMIT_SCRIPT="${M3_DUAL_EVAL_SUBMIT_SCRIPT:-${REPO_ROOT}/scripts/slurm/submit_m3_dual_domain_eval.sh}"
JOB_FILE="${M3_DUAL_EVAL_JOB_FILE:-${REPO_ROOT}/reports/m3/dual_domain_eval/job_matrix.tsv}"
STATE_FILE="${M3_DUAL_EVAL_STATE_FILE:-${REPO_ROOT}/reports/m3/dual_domain_eval/autosubmit_next_task.txt}"
LOG_FILE="${M3_DUAL_EVAL_AUTOSUBMIT_LOG:-${REPO_ROOT}/slurm_logs/m3_dual_eval_autosubmit.log}"

MAX_ACTIVE_JOBS="${M3_MAX_ACTIVE_JOBS:-15}"
CHUNK_LIMIT="${M3_DUAL_EVAL_AUTOSUBMIT_CHUNK:-15}"
SLEEP_SECONDS="${M3_DUAL_EVAL_AUTOSUBMIT_SLEEP:-300}"
DEFAULT_START="${M3_DUAL_EVAL_NEXT_TASK:-0}"

mkdir -p "$(dirname "$JOB_FILE")" "$(dirname "$STATE_FILE")" "$(dirname "$LOG_FILE")"
cd "$REPO_ROOT"

log() {
  printf '%s %s\n' "$(date -Is)" "$*" | tee -a "$LOG_FILE"
}

active_jobs() {
  squeue -u "$USER" -h -r 2>/dev/null | wc -l | sed 's/[[:space:]]//g'
}

min3() {
  local a="$1"
  local b="$2"
  local c="$3"
  local m="$a"
  if [ "$b" -lt "$m" ]; then m="$b"; fi
  if [ "$c" -lt "$m" ]; then m="$c"; fi
  echo "$m"
}

M3_DUAL_EVAL_MATRIX_ONLY=1 bash "$SUBMIT_SCRIPT" >> "$LOG_FILE" 2>&1
TASK_COUNT="$(wc -l < "$JOB_FILE" | sed 's/[[:space:]]//g')"

if [ "${M3_DUAL_EVAL_RESET_STATE:-0}" = "1" ] || [ ! -f "$STATE_FILE" ]; then
  NEXT_TASK="$DEFAULT_START"
else
  NEXT_TASK="$(cat "$STATE_FILE")"
fi

if [ "$NEXT_TASK" -lt 0 ] || [ "$NEXT_TASK" -gt "$TASK_COUNT" ]; then
  log "Invalid next task ${NEXT_TASK}; task count is ${TASK_COUNT}."
  exit 1
fi

echo "$NEXT_TASK" > "$STATE_FILE"
log "autosubmit start: next_task=${NEXT_TASK}, task_count=${TASK_COUNT}, cap=${MAX_ACTIVE_JOBS}, chunk_limit=${CHUNK_LIMIT}, sleep=${SLEEP_SECONDS}s"

while [ "$NEXT_TASK" -lt "$TASK_COUNT" ]; do
  ACTIVE="$(active_jobs)"
  HEADROOM=$((MAX_ACTIVE_JOBS - ACTIVE))
  REMAINING=$((TASK_COUNT - NEXT_TASK))

  if [ "$HEADROOM" -le 0 ]; then
    log "no headroom: active=${ACTIVE}, remaining=${REMAINING}; sleeping"
    sleep "$SLEEP_SECONDS"
    continue
  fi

  CHUNK="$(min3 "$CHUNK_LIMIT" "$HEADROOM" "$REMAINING")"
  log "submitting tasks ${NEXT_TASK}-$((NEXT_TASK + CHUNK - 1)): active=${ACTIVE}, headroom=${HEADROOM}, remaining=${REMAINING}"

  if M3_DUAL_EVAL_TASK_START="$NEXT_TASK" \
     M3_DUAL_EVAL_TASK_LIMIT="$CHUNK" \
     M3_DUAL_EVAL_ARRAY_CONCURRENCY="$CHUNK" \
     bash "$SUBMIT_SCRIPT" >> "$LOG_FILE" 2>&1; then
    NEXT_TASK=$((NEXT_TASK + CHUNK))
    echo "$NEXT_TASK" > "$STATE_FILE"
    log "submitted chunk; next_task=${NEXT_TASK}"
  else
    log "submit failed, likely no QOS headroom after scheduler refresh; sleeping"
  fi

  sleep "$SLEEP_SECONDS"
done

log "all ${TASK_COUNT} dual-domain eval tasks submitted"
