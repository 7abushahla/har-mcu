# M3 DeepConvLSTM Runbook

This document summarizes the Milestone 3 DeepConvLSTM implementation, notebooks, Slurm workflow, experiment outputs, and Arduino deployment path.

## What We Changed

The M3 work adds an operational experiment layer around the existing HAR/TinyML codebase while preserving the WISDM and paper-replication paths.

Code and config additions:

- `configs/m3/`: M3 experiment configs E00-E10. E01 user-holdout remains tooling-only and was not run.
- `src/m3/`: M3 orchestration, transfer experiments, reporting, and dataset build entry points.
- `src/data/load_har.py`, `src/data/resample.py`, `src/data/units.py`: WISDM-style CSV loading, resampling/downsampling, unit-mode handling, and metadata preservation.
- `src/data/build_dataset.py`, `src/data/load_wisdm.py`: M3-aware normalization, external/source normalization support, datacards, and split metadata.
- `src/utils/tflite_export.py`: shared TFLite conversion hardening for DeepConvLSTM, including fixed single-batch input shape handling where possible.
- `src/run_paper_experiment.py`, `src/quant/ptq_full_int8.py`, `src/quant/qat_train.py`: FP32 TFLite export, PTQ INT8, QAT INT8, TFLite host evaluation, and M3 report metadata.
- `src/eval/reporting.py` and `src/m3/reporting.py`: fixed-schema M3 report rows with FP32/PTQ/QAT metrics and deploy-gate status.
- `deploy/arduino_infer/arduino_infer.ino`: live IMU inference sketch using the exported model and normalization headers.
- `src/deploy/export_c_array.py`, `src/deploy/export_norm_header.py`: deployment header generation for `model_data.*` and `norm_stats.h`.
- `scripts/slurm/`: Slurm-first wrappers for dry runs, experiments, notebook checks, dataset builds, and deployment export.
- `notebooks/m3_deepconvlstm.ipynb` plus per-experiment notebooks `notebooks/m3_E*.ipynb`.
- `reports/m3/`: consolidated M3 reports, domain-gap summary, final deployment summary, and live-trial templates.

Current staged deployment headers:

- `deploy/common/model_data.h`
- `deploy/common/model_data.cc`
- `deploy/common/norm_stats.h`

These were regenerated from the E09 PTQ INT8 model and E09 Arduino fine-tune train-split normalization stats using Slurm job `7197`.

## What We Ran

All heavy work was submitted through GPU Slurm. No user-holdout experiments were run.

Completed full DeepConvLSTM jobs:

| Experiment | Job | Purpose | Status |
| --- | --- | --- | --- |
| E00 | `7186` | WISDM source-only M2 anchor | `COMPLETED 0:0` |
| E03 | `7188` | WISDM to Arduino zero-shot, 20 Hz T100 | `COMPLETED 0:0` |
| E04 | `7187` | WISDM-to-g plus Arduino-g unit convention | `COMPLETED 0:0` |
| E05 | `7190` | Legacy Arduino-to-m/s^2 negative control | `COMPLETED 0:0` |
| E06 | `7191` | Matched no-normalization ablation | `COMPLETED 0:0` |
| E07 | `7189` | Skip inference normalization diagnostic | `COMPLETED 0:0` |
| E08 | `7192` | T50 2.5-second window ablation | `COMPLETED 0:0` |
| E09 | `7194` | WISDM pretrain, Arduino fine-tune | `COMPLETED 0:0` |
| E10 | `7193` | Arduino from scratch | `COMPLETED 0:0` |

Notebook validation:

- `notebooks/m3_deepconvlstm.ipynb` was executed through Slurm jobs `7196` and `7198`.
- Latest notebook validation output: `notebooks/executed/m3_deepconvlstm.executed.latest.ipynb`.
- `notebooks/executed/` is generated validation output and should not be committed.

Deployment export:

- Slurm job `7197` regenerated `deploy/common/model_data.*` and `deploy/common/norm_stats.h`.

## Key Results

The aggregate report is:

- `reports/m3/m3_experiment_master.csv`
- `reports/m3/m3_experiment_master.md`

All nine full DeepConvLSTM runs exported:

- FP32 `.tflite`
- PTQ INT8 `.tflite`
- QAT INT8 `.tflite`

There are 27 full-run TFLite exports under `models_tflite/m3/`.

Current best non-diagnostic Arduino-target candidate:

- Experiment: `E09_wisdm_pretrain_arduino_finetune`
- Candidate export: PTQ INT8
- FP32 accuracy / macro-F1: `0.995575221238938` / `0.9955735520260941`
- PTQ accuracy / macro-F1: `0.9879898862199747` / `0.9880066511463083`
- QAT accuracy / macro-F1: `0.9298356510745891` / `0.9298920081134151`
- Deployment summary: `reports/m3/final_deployment_summary.md`

E07 is diagnostic-only and must not be selected as the final deployed model.

## Slurm And Environment Notes

The current workspace used:

```bash
/shared/b00088568/github/har-mcu
```

The current conda environment used inside Slurm jobs only:

```bash
/shared/b00088568/myenvs/tinymlproj
```

Other users may not have access to `b00088568` shared folders. They should use their own shared paths, for example:

```bash
export M3_REPO_ROOT=/shared/<your_user_or_project>/github/har-mcu
export M3_CONDA_ENV=/shared/<your_user_or_project>/myenvs/tinymlproj
```

The Slurm settings can stay structurally the same, but account/QOS may be user-specific:

```bash
export M3_SLURM_ACCOUNT=<your_account>
export M3_SLURM_QOS=<your_qos>
export M3_SLURM_PARTITION=gpu
export M3_SLURM_GRES=gpu:1
export M3_SLURM_CPUS=4
export M3_SLURM_MEM=15G
export M3_SLURM_TIME=48:00:00
```

For this project, keep heavy work on Slurm. Do not run host-node Python for training, evaluation, dataset loading, quantization, schema inspection, or TFLite evaluation.

## How To Run Experiments Directly

Submit from the repo root:

```bash
cd /shared/b00088568/github/har-mcu
source symbolic-motifgen/scripts/aus_hpc_env.sh
bash scripts/slurm/submit_m3_experiment.sh configs/m3/E09_wisdm_pretrain_arduino_finetune.yaml --artifact-suffix full_e09
```

Monitor jobs:

```bash
squeue -u $USER
sacct -j <JOBID> --format=JobID,JobName%45,State,ExitCode,Elapsed,Timelimit,Start,End -P
scontrol show job <JOBID>
find slurm_logs -type f | grep "\\.<JOBID>\\."
tail -n 50 slurm_logs/<log-file>.out
tail -n 50 slurm_logs/<log-file>.err
```

If Slurm assigns unhealthy GPU nodes, the wrappers support:

```bash
export M3_SLURM_EXCLUDE=gpu-dy-g5-0-83,gpu-dy-g5-0-88
```

## Notebook Overview

The notebooks are Slurm control surfaces. They are not meant to do heavy training locally in Jupyter.

Default behavior is safe: submission cells print the command but do not submit until the relevant flag is changed to `1`.

To run a notebook interactively:

1. Open the notebook.
2. Review the config and suffix at the top.
3. In the submission cell, change `SUBMIT_FULL_RUN=${SUBMIT_FULL_RUN:-0}` to `SUBMIT_FULL_RUN=1`, or launch Jupyter with that environment variable.
4. Run the submission cell.
5. Copy the Slurm job ID from the output.
6. In the monitor/log cells, set `JOBID=<job id>` or `JOBIDS="<job ids>"`.

You can also validate notebook execution itself through Slurm:

```bash
bash scripts/slurm/submit_m3_notebook_check.sh notebooks/m3_deepconvlstm.ipynb
```

## Notebook Details

| Notebook | Purpose | What It Runs | Main Outputs |
| --- | --- | --- | --- |
| `notebooks/m3_deepconvlstm.ipynb` | Main DeepConvLSTM M3 dashboard/control notebook | Lists configs, submits matrix dry run, submits smoke runs, submits full runs, monitors Slurm jobs, checks artifacts | `reports/m3/m3_experiment_master.*`, per-run `reports/m3/full_e*/`, `models_tflite/m3/**/full_e*/`, optional executed notebook under `notebooks/executed/` |
| `notebooks/m3_E00_wisdm_m2_anchor.ipynb` | WISDM source-only M2 anchor | `configs/m3/E00_wisdm_m2_anchor.yaml` with suffix `full_e00` | `reports/m3/full_e00/`, `models_tflite/m3/E00_wisdm_m2_anchor/full_e00/` |
| `notebooks/m3_E03_arduino_downsample_20hz_T100.ipynb` | Zero-shot WISDM to Arduino using current 20 Hz Arduino dataset, T100 | `configs/m3/E03_arduino_downsample_20hz_T100.yaml` with suffix `full_e03` | `reports/m3/full_e03/`, `models_tflite/m3/E03_arduino_downsample_20hz_T100/full_e03/` |
| `notebooks/m3_E04_wisdm_to_g_arduino_g.ipynb` | Unit convention ablation: convert WISDM to g and use Arduino g convention | `configs/m3/E04_wisdm_to_g_arduino_g.yaml` with suffix `full_e04` | `reports/m3/full_e04/`, `models_tflite/m3/E04_wisdm_to_g_arduino_g/full_e04/` |
| `notebooks/m3_E05_legacy_arduino_to_mps2.ipynb` | Legacy negative-control unit conversion | `configs/m3/E05_legacy_arduino_to_mps2.yaml` with suffix `full_e05` | `reports/m3/full_e05/`, `models_tflite/m3/E05_legacy_arduino_to_mps2/full_e05/` |
| `notebooks/m3_E06_no_norm_matched.ipynb` | Matched no-normalization training/inference ablation | `configs/m3/E06_no_norm_matched.yaml` with suffix `full_e06` | `reports/m3/full_e06/`, `models_tflite/m3/E06_no_norm_matched/full_e06/` |
| `notebooks/m3_E07_skip_inference_norm_diag.ipynb` | Diagnostic skip-inference-normalization ablation | `configs/m3/E07_skip_inference_norm_diag.yaml` with suffix `full_e07` | `reports/m3/full_e07/`, `models_tflite/m3/E07_skip_inference_norm_diag/full_e07/`; diagnostic-only, not deploy eligible |
| `notebooks/m3_E08_T50_window.ipynb` | T50 2.5-second window-size ablation | `configs/m3/E08_T50_window.yaml` with suffix `full_e08` | `reports/m3/full_e08/`, `models_tflite/m3/E08_T50_window/full_e08/` |
| `notebooks/m3_E09_wisdm_pretrain_arduino_finetune.ipynb` | WISDM pretrain then Arduino fine-tune | `configs/m3/E09_wisdm_pretrain_arduino_finetune.yaml` with suffix `full_e09` | `reports/m3/full_e09/`, `models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/full_e09/`, deployment candidate |
| `notebooks/m3_E10_arduino_from_scratch.ipynb` | Train only on the collected Arduino dataset | `configs/m3/E10_arduino_from_scratch.yaml` with suffix `full_e10` | `reports/m3/full_e10/`, `models_tflite/m3/E10_arduino_from_scratch/full_e10/` |

E01 user-holdout tooling exists in config form but was not run. E02 true-100-Hz Arduino zero-shot exists in config form but was not run because the current merged Arduino CSVs are 20 Hz, not true 100 Hz.

## Arduino Fine-Tune And From-Scratch Tooling

Yes, the requested Arduino adaptation path is implemented.

For WISDM pretrain plus Arduino fine-tune:

```bash
bash scripts/slurm/submit_m3_experiment.sh configs/m3/E09_wisdm_pretrain_arduino_finetune.yaml --artifact-suffix full_e09
```

This trains on WISDM first, fine-tunes on the Arduino train split, evaluates on untouched Arduino test split, exports FP32/PTQ/QAT TFLite, evaluates host-side TFLite, and writes reports.

For Arduino-only from scratch:

```bash
bash scripts/slurm/submit_m3_experiment.sh configs/m3/E10_arduino_from_scratch.yaml --artifact-suffix full_e10
```

This trains only on the Arduino train split, evaluates on untouched Arduino test split, exports FP32/PTQ/QAT TFLite, evaluates host-side TFLite, and writes reports.

The Arduino test split must not be used for normalization, calibration, representative data, QAT fine-tuning, early stopping, or hyperparameter selection.

## Hz And Window Matching Clarification

WISDM M2 baseline:

- 20 Hz
- T100
- 5-second windows
- 50% overlap

Current Arduino dataset:

- The merged Arduino CSVs currently used by M3 are treated as 20 Hz WISDM-style CSVs.
- E03, E04, E05, E06, E07, E09, and E10 run with T100 at 20 Hz.
- E08 runs T50 at 20 Hz for the 2.5-second window ablation.

What we matched:

- We matched the current Arduino dataset to the WISDM-compatible 20 Hz/T100 path for the main transfer and adaptation experiments.
- We kept 50% overlap.
- We evaluated unit convention matching in E04 by converting WISDM to g and keeping Arduino in g-style units.
- We evaluated the legacy opposite convention in E05 as a negative-control style ablation.

What we did not run:

- We did not run true Arduino 100 Hz T500 because the current merged Arduino source available to the repo is already 20 Hz.
- We did not upsample WISDM to 100 Hz.
- We did not run E01 user-holdout experiments.

## On-Device Deployment Integration

The live Arduino sketch uses:

- `deploy/arduino_infer/arduino_infer.ino`
- `deploy/common/model_data.h`
- `deploy/common/model_data.cc`
- `deploy/common/norm_stats.h`

Regenerate deployment headers from the selected model through Slurm:

```bash
bash scripts/slurm/submit_m3_deploy_export.sh \
  models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/full_e09/deepconv_lstm_conv2d_T100_Prandom_stratified_E09_deepconv_lstm_r0_ptq_int8.tflite \
  data/processed/m3/E09_wisdm_pretrain_arduino_finetune/full_e09/finetune_arduino/norm_stats_T100_Prandom_stratified.json \
  deploy/common
```

The generated `norm_stats.h` controls:

- `WINDOW_SIZE`
- `SAMPLE_RATE_HZ`
- `APPLY_NORMALIZATION`
- `UNIT_PRE_MULTIPLY`
- `UNIT_SCALE`
- per-axis mean/std
- unit and normalization mode strings

Compile and flash when Arduino CLI and board libraries are installed:

```bash
arduino-cli compile --fqbn arduino:mbed_nano:nano33ble deploy/arduino_infer
arduino-cli upload -p <PORT> --fqbn arduino:mbed_nano:nano33ble deploy/arduino_infer
```

Record serial logs:

```bash
arduino-cli monitor -p <PORT> -c baudrate=115200 > reports/m3/live_trial_E09_ptq.csv
```

Expected sketch serial rows:

```text
timestamp_ms,label,confidence,invoke_ms,e2e_ms
```

Use `reports/m3/live_trial_template.csv` and `docs/m3_live_trial_protocol.md` for live testing. The sketch should print `tensor_arena_bytes` at setup and average invoke latency after at least 50 inferences.

## Files And Folders Not To Commit

Do not commit or push:

- `slurm_logs/`
- PDF files such as `*.pdf` or `*.PDF`
- `DeepConv+LSTM.ipynb`
- generated processed arrays under `data/processed/`
- executed notebook outputs under `notebooks/executed/`
- smoke-run artifacts under `reports/m3/smoke*/`
- smoke-run TFLites under `models_tflite/m3/*/smoke*/`

The first three exclusions were explicitly requested for this repo handoff. The generated data and executed notebook outputs are also local/reproducible artifacts and are ignored to keep the Git history lightweight.
