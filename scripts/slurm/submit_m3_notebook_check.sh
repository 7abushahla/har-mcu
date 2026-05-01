#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -lt 1 ]; then
  echo "Usage: bash scripts/slurm/submit_m3_notebook_check.sh notebooks/m3_deepconvlstm.ipynb [output_name.ipynb]" >&2
  exit 2
fi

NOTEBOOK="$1"
OUTPUT_NAME="${2:-$(basename "$NOTEBOOK" .ipynb).executed.ipynb}"

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
TIME_LIMIT="${M3_SLURM_TIME:-04:00:00}"
MAX_ACTIVE_JOBS="${M3_MAX_ACTIVE_JOBS:-15}"
EXCLUDE="${M3_SLURM_EXCLUDE:-}"
SBATCH_EXCLUDE_LINE=""
if [ -n "$EXCLUDE" ]; then
  SBATCH_EXCLUDE_LINE="#SBATCH --exclude=${EXCLUDE}"
fi

ACTIVE_JOBS="$(squeue -u "$USER" -h 2>/dev/null | wc -l | sed 's/[[:space:]]//g')"
if [ "${ACTIVE_JOBS:-0}" -ge "$MAX_ACTIVE_JOBS" ]; then
  echo "Refusing to submit: active jobs (${ACTIVE_JOBS}) >= cap (${MAX_ACTIVE_JOBS})." >&2
  exit 1
fi

mkdir -p "$REPO_ROOT/slurm_logs" "$REPO_ROOT/notebooks/executed"
JOB_BASENAME="$(basename "$NOTEBOOK" .ipynb)"

sbatch <<SBATCH
#!/usr/bin/env bash
#SBATCH --job-name=m3_nb_${JOB_BASENAME}
#SBATCH --account=${ACCOUNT}
#SBATCH --qos=${QOS}
#SBATCH --partition=${PARTITION}
#SBATCH --gres=${GRES}
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

jupyter nbconvert \
  --to notebook \
  --execute "${NOTEBOOK}" \
  --output-dir "${REPO_ROOT}/notebooks/executed" \
  --output "${OUTPUT_NAME}" \
  --ExecutePreprocessor.timeout=600
SBATCH
