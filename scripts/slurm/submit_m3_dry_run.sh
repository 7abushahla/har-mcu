#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: bash scripts/slurm/submit_m3_dry_run.sh configs/m3/E00_wisdm_m2_anchor.yaml" >&2
  exit 2
fi

CONFIG="$1"
shift || true

if [ -f symbolic-motifgen/scripts/aus_hpc_env.sh ]; then
  source symbolic-motifgen/scripts/aus_hpc_env.sh
elif [ -f ../symbolic-motifgen/scripts/aus_hpc_env.sh ]; then
  source ../symbolic-motifgen/scripts/aus_hpc_env.sh
fi

REPO_ROOT="${M3_REPO_ROOT:-/shared/b00088568/github/har-mcu}"
CONDA_ENV="${M3_CONDA_ENV:-/shared/b00088568/myenvs/tinymlproj}"
ACCOUNT="${M3_SLURM_ACCOUNT:-acc-izualkernan}"
QOS="${M3_SLURM_QOS:-gpu-medium-izualkernan-001}"
PARTITION="${M3_SLURM_DRYRUN_PARTITION:-gpu}"
GRES="${M3_SLURM_DRYRUN_GRES:-gpu:1}"
CPUS="${M3_SLURM_CPUS:-4}"
MEM="${M3_SLURM_MEM:-15G}"
TIME_LIMIT="${M3_SLURM_DRYRUN_TIME:-04:00:00}"
MAX_ACTIVE_JOBS="${M3_MAX_ACTIVE_JOBS:-15}"
SBATCH_GRES_LINE=""
if [ -n "$GRES" ]; then
  SBATCH_GRES_LINE="#SBATCH --gres=${GRES}"
fi

ACTIVE_JOBS="$(squeue -u "$USER" -h 2>/dev/null | wc -l | sed 's/[[:space:]]//g')"
if [ "${ACTIVE_JOBS:-0}" -ge "$MAX_ACTIVE_JOBS" ]; then
  echo "Refusing to submit: active jobs (${ACTIVE_JOBS}) >= cap (${MAX_ACTIVE_JOBS})." >&2
  exit 1
fi

mkdir -p "$REPO_ROOT/slurm_logs"
JOB_BASENAME="$(basename "$CONFIG" .yaml)"
JOB_NAME="m3dry_${JOB_BASENAME}"

sbatch <<SBATCH
#!/usr/bin/env bash
#SBATCH --job-name=${JOB_NAME}
#SBATCH --account=${ACCOUNT}
#SBATCH --qos=${QOS}
#SBATCH --partition=${PARTITION}
${SBATCH_GRES_LINE}
#SBATCH --cpus-per-task=${CPUS}
#SBATCH --mem=${MEM}
#SBATCH --time=${TIME_LIMIT}
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
python -m src.m3.run_experiment --config "${CONFIG}" --dry-run
SBATCH
