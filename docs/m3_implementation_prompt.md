# Milestone 3 Implementation Prompt

You are working in the GitHub repo `7abushahla/har-mcu`.

Use branch `ariel-test` as the implementation branch. Use branch `layth-arduino` only as a source/reference for Arduino-collected data and Tiny Motion conversion utilities. Do not remove the existing WISDM baseline, notebooks, or paper-replication paths.

## HPC/Slurm Operating Rules

You are working in `/shared/b00088568/github/har-mcu`.

Submit all heavy work through Slurm only. Do not run host-node Python for training, evaluation, data loading, dataset/schema inspection, quantization, notebook execution, or TFLite evaluation. Do not use `pytest` on the host node. Do not use `rg`; use host-safe shell inspection commands such as `grep`, `find`, `sed`, `tail`, `wc`, `ls`, `squeue`, `sacct`, and `scontrol`.

Shared environment root:

- `/shared/b00088568/myenvs`

Use this conda environment inside Slurm jobs only:

- `/shared/b00088568/myenvs/tinymlproj`

Do not use the old `pipeline` environment for this HAR/TinyML project unless explicitly instructed.

Current Slurm association and defaults:

- Account: `acc-izualkernan`.
- Default QOS: `gpu-medium-izualkernan-001`.
- QOS submit cap: `15`.
- Reported `MaxTRES`: `node=10`.
- Global GPU defaults from `aus_hpc_env.sh`: `partition=gpu`, `gres=gpu:1`, `cpus=4`, `mem=15G`, `time_train=48:00:00`, `time_eval=04:00:00`.
- Common CPU convention: `partition=cpu`, no GRES, `cpus=4`, `mem=15G`, wallclock usually `4h-12h` for eval/backfill.

Submit from the host node by sourcing:

```bash
source symbolic-motifgen/scripts/aus_hpc_env.sh
```

Then call the appropriate `submit_*.sh` wrapper. Inside each Slurm job, activate the environment with:

```bash
conda activate /shared/b00088568/myenvs/tinymlproj
```

Check jobs with:

```bash
squeue -u $USER
sacct -j <JOBID> --format=JobID,JobName%45,State,ExitCode,Elapsed,Timelimit,Start,End -P
scontrol show job <JOBID>
```

For logs:

```bash
find slurm_logs -type f | grep "\\.<JOBID>\\."
tail -n 50 <matching-log>.out
tail -n 50 <matching-log>.err
```

Keep active jobs at or below `15`.

## Current Repo Structure To Respect

This repo already has a WISDM-first TinyML HAR pipeline. Extend it instead of creating a disconnected second pipeline.

Important existing paths:

- `WISDM_ar_v1.1/WISDM_ar_v1.1_raw.csv`: primary WISDM raw CSV.
- `wisdm_overview.ipynb` and `notebooks/wisdm_overview.ipynb`: WISDM exploration notebooks.
- `tiny-motion/`: Arduino/Tiny Motion data conversion utilities and Arduino-collected CSV/JSON data.
- `arduino-code/`: Arduino libraries plus `tf4micro-motion-kit` reference firmware/source.
- `configs/default.yaml`: current DeepConvLSTM WISDM config.
- `configs/papers/*.yaml`: existing paper replication configs.
- `src/data/load_wisdm.py`: current WISDM-style CSV loader.
- `src/data/preprocess_zhou2025.py`: current null/drop-zero/sort preprocessing.
- `src/data/windowing.py`: current window generator with 50% overlap support.
- `src/data/splits.py`: current `random_stratified` and `user_holdout` split implementations.
- `src/data/normalize.py`: current train-only per-axis z-score helpers.
- `src/data/build_dataset.py`: current processed dataset builder and datacard/norm-stats writer.
- `src/train/train_model.py`: architecture-agnostic Keras training path.
- `src/run_paper_experiment.py`: model-variant registry and FP32 -> FP32 TFLite -> PTQ -> QAT -> report path for paper models.
- `src/quant/ptq_full_int8.py` and `src/quant/qat_train.py`: quantization paths.
- `src/eval/evaluate_model.py` and `src/eval/eval_tflite.py`: FP32 and TFLite evaluation/reporting.
- `src/deploy/export_c_array.py` and `src/deploy/export_norm_header.py`: model/norm C header export.
- `deploy/common/model_data.h`, `deploy/common/model_data.cc`, `deploy/common/norm_stats.h`: current deployment headers.
- `deploy/arduino_infer/arduino_infer.ino`: current live inference sketch.
- `tests/`: existing regression tests for splits, windowing, normalization, reports, TFLite timing, QAT/PTQ paths, config contracts, and deploy gates.

Current known model variants are implemented under `src/models/`. Reuse their existing builders/configs:

- `deepconv_lstm` and the Conv2D-safe variant in `src/models/deepconv_lstm.py`.
- `daghero_cnn_2layer_conv2d`.
- `repmobile_folded_conv2d`.
- `tcn_attention_har_teacher_conv2d`.
- `tcn_inception_conv2d`.
- `xtinyhar_student_conv2d`.

The existing paper configs often use `window_size_default: 200` for paper replication. Milestone 3 must support the M2/M3 windows explicitly: `T=100` and `T=50` at 20 Hz, and `T=500` at 100 Hz for a 5 s Arduino duration-matched setting.

## Arduino Dataset Files

Use the merged Arduino WISDM-style CSV with numeric users as the default Arduino dataset for fine-tuning/evaluation:

- Primary Arduino fine-tuning/evaluation CSV: `tiny-motion/Arduino_layth_hamza_wisdm_raw_numeric_user.csv`.
- Provenance/debug equivalent with string users: `tiny-motion/Arduino_layth_hamza_wisdm_raw.csv`.
- Legacy negative-control m/s^2 CSVs: `tiny-motion/Arduino_layth_hamza_wisdm_mps2_numeric_user.csv` and `tiny-motion/Arduino_layth_hamza_wisdm_mps2.csv`.

Observed dataset facts:

- Both raw Arduino CSVs use WISDM-style columns: `user, activity, timestamp, x-axis, y-axis, z-axis`.
- `Arduino_layth_hamza_wisdm_raw_numeric_user.csv` has numeric users `37` and `38`; prefer it because the current windowing/split code expects users to be castable to integers.
- `Arduino_layth_hamza_wisdm_raw.csv` has users `layth` and `hamza`; if this path is used, map names to stable integer IDs before calling the current `generate_windows`.
- Both raw Arduino CSVs have 240,620 rows, six classes, and synthetic 50,000,000 ns timestamp steps, so they are already WISDM-compatible 20 Hz merged files.
- The raw Arduino CSV axes are small-magnitude stored values, roughly within `[-1, 1]`, consistent with Tiny Motion/tf4micro-style storage. Do not silently convert them.
- The `mps2` Arduino CSVs are already scaled to approximately `stored * 4 * 9.80665`; use them only for the explicit legacy/negative-control experiment.
- Conversion utilities are in `tiny-motion/json_to_wisdm_csv.py` and `tiny-motion/merge_arduino_wisdm.py`. These document the firmware `/4` storage convention and the optional `--acc-pre-multiply 4` and `--acc-scale 9.80665` choices.

## Project Context

- This is a TinyML HAR project for Arduino Nano 33 BLE Sense.
- M2 baseline: WISDM v1.1, six classes, accelerometer-only, 20 Hz, `T=100` samples = 5 s, 50% overlap, train-only z-score normalization, random-stratified train/validation/test split.
- M3 requires live Arduino inference, deployment metrics, optimization, live on-device accuracy, robustness testing, and an updated repo.
- Keep the class order exactly:

```python
["Walking", "Jogging", "Upstairs", "Downstairs", "Sitting", "Standing"]
```

- Keep overlap at `0.5` for all M3 experiments.
- Use `random_stratified` as the primary M3 split with the current correct train/validation/test split semantics: test split first, validation split from train-val only.
- Set up tooling support for `user_holdout`/user-disjoint, but do not run user-holdout experiments unless explicitly re-enabled by the project owner. `configs/m3/E01_wisdm_user_holdout.yaml` is tooling-only/disabled by default.
- Do not remove or break existing WISDM and paper-replication paths.

## Implementation Strategy

Implement the Milestone 3 operational layer in phases:

1. Make one stable DeepConvLSTM live Arduino demo work first.
2. Once DeepConvLSTM works end to end, apply the same config and reporting contract across the other architectures.
3. Use the test set only for final offline comparison and report which architecture does best.

Priority order:

1. DeepConvLSTM source-only WISDM anchor.
2. DeepConvLSTM zero-shot WISDM -> Arduino.
3. DeepConvLSTM Arduino 20 Hz downsample/WISDM-compatible run.
4. DeepConvLSTM unit and normalization ablations.
5. DeepConvLSTM fine-tune and Arduino-from-scratch runs.
6. Deploy one stable model to Arduino and record live metrics.
7. Expand the same configs to Daghero, RepMobile, TCN-attention, TCN-Inception, and XTinyHAR.

## Required M3 Capabilities

### 1. Data/source support

Add explicit support for WISDM-only, Arduino-only, and WISDM+Arduino transfer experiments.

Use these config concepts:

- `data.source`: `wisdm`, `arduino`, or `wisdm_arduino`.
- `paths.wisdm_raw_csv`: default `WISDM_ar_v1.1/WISDM_ar_v1.1_raw.csv`.
- `paths.arduino_raw_csv`: default `tiny-motion/Arduino_layth_hamza_wisdm_raw_numeric_user.csv`.
- Keep `paths.raw_csv` backward-compatible for existing WISDM scripts.

Implement or extend a loader that accepts WISDM-style CSVs with columns:

```text
user,activity,timestamp,x-axis,y-axis,z-axis
```

Preserve metadata through datacards and experiment artifacts:

- `domain`: `wisdm` or `arduino`.
- `user_id`.
- `original_sample_rate_hz`.
- `target_sample_rate_hz`.
- `unit_mode`.
- `source_csv`.
- row counts and class counts.

Do not force the existing WISDM loader to become Arduino-only. The clean approach is likely a general `src/data/load_har_csv.py` or equivalent used by `build_dataset`, with `load_wisdm.py` kept as a backward-compatible wrapper.

### 2. Sampling-rate support

Add config keys:

- `data.sample_rate_hz`.
- `data.target_sample_rate_hz`.
- `data.downsample`.

Add downsampling/resampling utilities under `src/data/`, and record all choices in datacards.

Support:

- WISDM baseline: 20 Hz, `T=100`, 5 s windows.
- Arduino WISDM-compatible merged CSV: 20 Hz, `T=100`, 5 s windows.
- Arduino 100 Hz as-is, if using true 100 Hz source data: 100 Hz, `T=500`, 5 s windows.
- Arduino 100 Hz sample-matched diagnostic: 100 Hz, `T=100`, 1 s windows.
- `T=50` at 20 Hz: 2.5 s windows.

Always report:

- `window_size_samples`.
- `window_duration_seconds`.
- `sample_rate_hz`.
- `target_sample_rate_hz`.
- whether downsampling/resampling was applied.

Important: the current merged Arduino files under `tiny-motion/Arduino_layth_hamza_wisdm_raw*.csv` have 50 ms timestamp steps and should be treated as WISDM-compatible 20 Hz files unless a different raw 100 Hz source is explicitly selected.

### 3. Unit convention support

Implement explicit unit modes. Never silently convert units.

- `raw_no_conversion`: leave source axes as stored.
- `arduino_g`: if Arduino values came from tf4micro-motion-kit storage, undo firmware `/4` by multiplying by `4.0`, but do not multiply by `9.80665`.
- `wisdm_to_g`: convert WISDM axes to `g` using configurable factor, default `9.80665` unless overridden. Do not convert Arduino to m/s^2 in this mode.
- `arduino_to_mps2_legacy`: legacy/negative-control mode that converts Arduino stored values to m/s^2, normally `stored * 4.0 * 9.80665`.

Log exact scale factors into every datacard and experiment artifact:

- per-domain scale.
- pre-multiply scale.
- unit scale.
- final total scale per axis if axis-specific scaling is added later.

### 4. Normalization support

Keep valid default normalization as train-only per-axis z-score.

Add config:

- `normalization.mode`: `train_zscore` or `none`.
- `normalization.diagnostic_skip_inference_norm`: `true` or `false`.

Requirements:

- No validation/test/Arduino-test statistics may be used to fit normalization.
- Save `norm_stats.json` for every experiment/run, including metadata when normalization is `none`.
- Regenerate `deploy/common/norm_stats.h` from the selected final `norm_stats.json`.
- If `diagnostic_skip_inference_norm: true`, mark output artifacts as `diagnostic_only: true`.
- Diagnostic-only artifacts must not be selectable as the final deployed model.
- Do not make no-normalization-at-inference the final deployed model unless training also used no normalization.

### 5. Window-size support

Support:

- `T=100` at 20 Hz, 5 s windows.
- `T=50` at 20 Hz, 2.5 s windows.
- `T=500` at 100 Hz, 5 s windows when true 100 Hz Arduino data is used.

Keep overlap `0.5`.

Ensure artifact names include:

- model variant.
- data source/domain.
- transfer mode.
- sample rate.
- target sample rate.
- `T`.
- split protocol.
- run ID.

Do not let the current `dataset_prefix(T, protocol)` naming collide across WISDM-only, Arduino-only, and transfer experiments. Extend artifact naming rather than overwriting existing `data/processed/T*_P*.npy` files.

### 6. Transfer learning support

Add training/evaluation paths for:

- `source_only`: train on WISDM, evaluate on WISDM.
- `zero_shot`: train on WISDM, evaluate on held-out Arduino data without tuning.
- `finetune`: pretrain on WISDM, fine-tune on Arduino train split, evaluate on untouched Arduino test split.
- `arduino_from_scratch`: train only on Arduino train split, evaluate on untouched Arduino test split.

Hard guardrail:

The Arduino held-out test split must never be used for normalization, calibration, hyperparameter selection, representative data, QAT fine-tuning, or early stopping.

Prefer adding an M3 orchestration module such as `src/m3/run_experiment.py` or `src/run_m3_experiment.py` that reuses:

- dataset build/load functions from `src/data`.
- training from `src/train/train_model.py`.
- model registry logic from `src/run_paper_experiment.py` or a shared registry helper.
- quantization from `src/quant`.
- evaluation from `src/eval`.
- deployment export from `src/deploy`.

### 7. Model/quantization sweep

For each selected model:

- Train FP32.
- Export FP32 TFLite.
- Run PTQ INT8.
- Run QAT INT8 if enabled.
- Evaluate host-side TFLite.
- Save accuracy, macro-F1, per-class metrics, confusion matrix, model size KB, latency summaries, input/output dtype, interpreter ops, and deploy-gate status.

Start with DeepConvLSTM. Once stable, run the same config matrix across:

- `daghero_cnn_2layer_conv2d`.
- `repmobile_folded_conv2d`.
- `tcn_attention_har_teacher_conv2d`.
- `tcn_inception_conv2d`.
- `xtinyhar_student_conv2d`.

### 8. Deployment export

For the chosen final model:

- Export `.tflite`.
- Export `deploy/common/model_data.h`.
- Export `deploy/common/model_data.cc`.
- Export `deploy/common/norm_stats.h`.
- Update `deploy/arduino_infer/arduino_infer.ino` if necessary.

The Arduino sketch must:

- Read live IMU accelerometer data.
- Enforce configured sample rate with timing control.
- Maintain a ring buffer of `WINDOW_SIZE x 3`.
- Apply the same unit and normalization convention used in training.
- Invoke TFLite Micro only when a full window and hop are available.
- Print serial CSV-like rows:

```text
timestamp_ms,label,confidence,invoke_ms,e2e_ms
```

- Accumulate and print average invoke latency over at least 50 inferences.
- Print `tensor_arena_bytes` during setup.

The current sketch already has a ring buffer, normalization, model invocation, and tensor arena print. It still needs stricter configured sample-rate timing, CSV-like serial output, unit-mode handling, and average latency reporting.

### 9. Reports/artifacts

Create:

- `reports/m3/m3_experiment_master.csv`.
- `reports/m3/m3_experiment_master.md`.
- `reports/m3/domain_gap_summary.csv`.
- `reports/m3/final_deployment_summary.md`.
- `reports/m3/live_trial_template.csv`.
- `docs/m3_live_trial_protocol.md`.

Each experiment row must include:

```text
experiment_id, model_variant, data_source, train_domain, eval_domain,
sample_rate_hz, target_sample_rate_hz, downsample, window_size_samples,
window_duration_seconds, overlap, unit_mode, normalization_mode,
inference_norm_applied, split_protocol, transfer_mode, seed,
fp32_accuracy, fp32_macro_f1, ptq_accuracy, ptq_macro_f1,
qat_accuracy, qat_macro_f1, model_size_kb, latency_mean_ms,
latency_median_ms, latency_p95_ms, deploy_gate_status, notes
```

`final_deployment_summary.md` must include exact commands to reproduce:

- dataset build.
- training.
- quantization.
- export.
- Arduino compile.
- flashing.
- serial logging.

### 10. Experiment matrix to implement

Add configs under `configs/m3/`:

- `E00_wisdm_m2_anchor.yaml`.
- `E01_wisdm_user_holdout.yaml`.
- `E02_arduino_zero_shot_100hz_T500.yaml`.
- `E03_arduino_downsample_20hz_T100.yaml`.
- `E04_wisdm_to_g_arduino_g.yaml`.
- `E05_legacy_arduino_to_mps2.yaml`.
- `E06_no_norm_matched.yaml`.
- `E07_skip_inference_norm_diag.yaml`.
- `E08_T50_window.yaml`.
- `E09_wisdm_pretrain_arduino_finetune.yaml`.
- `E10_arduino_from_scratch.yaml`.

Use DeepConvLSTM as the default model for these configs first. Add a way to override `experiment.model_variant` or run the same config matrix across all supported model variants after DeepConvLSTM works.

### 11. Guardrails

- Do not change the six-class label order.
- Do not use test-set statistics for normalization.
- Do not use Arduino test data for representative calibration.
- Do not use Arduino test data for early stopping or hyperparameter decisions.
- Do not silently convert units.
- Do not make no-normalization-at-inference the final deployed model unless training also used no normalization.
- Do not let diagnostic-only artifacts pass the final deployment selection gate.
- Do not make every ablation block the M3 demo. Produce one stable live Arduino demo first, then run broader ablations.
- Keep all generated artifacts reproducible with config files and run IDs.
- Preserve the existing WISDM paper-replication configs and outputs.
- Preserve backward compatibility for existing tests unless intentionally updating tests to match a new explicit contract.

### 12. Acceptance checks

Implement tests or CLI checks so these pass:

- A dry run lists all M3 configs and validates required keys.
- Building WISDM `T=100` `random_stratified` still works.
- User-holdout tooling remains available and disabled by default; do not submit user-holdout builds or experiments unless explicitly approved. If approval is later given, WISDM `T=100` `user_holdout` must produce no user overlap across train/val/test.
- Arduino data build produces class counts and domain metadata.
- The numeric-user Arduino CSV is selected by default for fine-tuning/evaluation.
- Unit-mode scale factors are present in every datacard.
- `norm_stats.json` and `norm_stats.h` match for the final model.
- `model_data.h` and `model_data.cc` are regenerated from the selected `.tflite`.
- `deploy/arduino_infer/arduino_infer.ino` compiles when Arduino CLI/libraries are installed.
- `final_deployment_summary.md` includes exact reproduction commands.

## Suggested First Commands

Use these host-node commands only for lightweight orientation:

```bash
ls
find configs src docs scripts -maxdepth 3 -type f | sort
grep -R "random_stratified" -n configs src tests | sed -n '1,120p'
squeue -u $USER
```

After implementing M3 config validation, add Slurm wrappers for dry runs instead of running host-node Python directly. Submit from the host node with:

```bash
source symbolic-motifgen/scripts/aus_hpc_env.sh
bash scripts/slurm/submit_m3_dry_run.sh configs/m3/E00_wisdm_m2_anchor.yaml
bash scripts/slurm/submit_m3_matrix_dry_run.sh configs/m3
```

Inside the submitted Slurm job, the command may be:

```bash
conda activate /shared/b00088568/myenvs/tinymlproj
python -m src.m3.run_experiment --config configs/m3/E00_wisdm_m2_anchor.yaml --dry-run
python -m src.m3.run_matrix --config-dir configs/m3 --dry-run
```

Submit dataset builds through the GPU-default Slurm wrapper, not host-node Python:

```bash
source symbolic-motifgen/scripts/aus_hpc_env.sh
bash scripts/slurm/submit_m3_build_dataset.sh configs/m3/E00_wisdm_m2_anchor.yaml --split-protocol random_stratified
```

The dataset-build wrapper now defaults to GPU Slurm resources and refuses user-holdout work unless `M3_ALLOW_USER_HOLDOUT=1` is explicitly set after project-owner approval.

Then proceed with DeepConvLSTM only before expanding, again through Slurm wrappers:

```bash
source symbolic-motifgen/scripts/aus_hpc_env.sh
bash scripts/slurm/submit_m3_experiment.sh configs/m3/E00_wisdm_m2_anchor.yaml
bash scripts/slurm/submit_m3_experiment.sh configs/m3/E03_arduino_downsample_20hz_T100.yaml
bash scripts/slurm/submit_m3_experiment.sh configs/m3/E09_wisdm_pretrain_arduino_finetune.yaml
```

Inside the submitted Slurm jobs, the commands may be:

```bash
conda activate /shared/b00088568/myenvs/tinymlproj
python -m src.m3.run_experiment --config configs/m3/E00_wisdm_m2_anchor.yaml
python -m src.m3.run_experiment --config configs/m3/E03_arduino_downsample_20hz_T100.yaml
python -m src.m3.run_experiment --config configs/m3/E09_wisdm_pretrain_arduino_finetune.yaml
```
