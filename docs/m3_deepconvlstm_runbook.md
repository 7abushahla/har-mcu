# M3 DeepConvLSTM And Architecture Sweep Runbook

This document summarizes the Milestone 3 DeepConvLSTM implementation, all-architecture sweep workflow, notebooks, Slurm workflow, experiment outputs, accelerometer-rotation augmentation runs, dual-domain evaluation, and Arduino deployment path.

For the code-level end-to-end training, validation, evaluation, quantization, and deployment contract, see `docs/m3_end_to_end_pipeline.md`.

## What We Changed

The M3 work adds an operational experiment layer around the existing HAR/TinyML codebase while preserving the WISDM and paper-replication paths.

Code and config additions:

- `configs/m3/`: M3 experiment configs E00-E12. E01 user-holdout remains tooling-only and was not run; E02 remains the future true-100-Hz Arduino path.
- `src/m3/`: M3 orchestration, transfer experiments, reporting, and dataset build entry points.
- `src/data/load_har.py`, `src/data/resample.py`, `src/data/units.py`: WISDM-style CSV loading, resampling/downsampling, unit-mode handling, and metadata preservation.
- `src/data/build_dataset.py`, `src/data/load_wisdm.py`: M3-aware normalization, external/source normalization support, datacards, and split metadata.
- `src/utils/tflite_export.py`: shared TFLite conversion hardening for DeepConvLSTM, including fixed single-batch input shape handling where possible.
- `src/run_paper_experiment.py`, `src/quant/ptq_full_int8.py`, `src/quant/qat_train.py`: FP32 TFLite export, PTQ INT8, QAT INT8, TFLite host evaluation, and M3 report metadata.
- `src/train/augment.py`: training-only accelerometer window rotation. It supports v1 `uniform_so3`, v2 `bounded_so3`, and v3 `target_gravity`. Each policy samples one rotation per selected `[T, 3]` training window, denormalizes with the saved train-split mean/std, rotates in raw accelerometer units, and re-applies the same normalization. Validation, test, PTQ representative data, and inference/on-device preprocessing are untouched. QAT uses this same training-input path when `augment.accel_rotation.apply_in_qat=true`. The rotation-augmentation idea follows orientation-robust HAR literature, especially Yurtman and Barshan 2017 (`10.3390/s17081838`), Yurtman, Barshan, and Fidan 2018 (`10.3390/s18082725`), and Caramaschi, Papini, and Caiani 2023 (`10.3390/app13074175`).
- `src/m3/dual_domain_eval.py`: eval-only comparison runner for the augmentation off/on table. It evaluates FP32, PTQ, and QAT TFLite exports against both WISDM and Arduino test splits while normalizing each eval dataset with the trained model's saved train-split stats.
- `src/m3/axis_eda.py`: axis-level WISDM-vs-Arduino EDA. It summarizes sample distributions, window-level gravity proxies, dynamic energy, and dominant-axis patterns so the next augmentation is based on observed domain shifts rather than guessed rotations.
- `src/eval/reporting.py` and `src/m3/reporting.py`: fixed-schema M3 report rows with FP32/PTQ/QAT metrics and deploy-gate status.
- `deploy/arduino_infer/arduino_infer.ino`: live IMU inference sketch using the exported model and normalization headers.
- `src/deploy/export_c_array.py`, `src/deploy/export_norm_header.py`: deployment header generation for `model_data.*` and `norm_stats.h`.
- `scripts/slurm/`: Slurm-first wrappers for dry runs, experiments, notebook checks, dataset builds, deployment export, and architecture sweeps.
- `scripts/slurm/submit_m3_accel_rotation_runs.sh`: submits the DeepConvLSTM and Daghero augmented training matrix.
- `scripts/slurm/submit_m3_rotation_ablation_train.sh`: submits the clean full-dataset DeepConvLSTM/Daghero augmentation off/on training matrix.
- `scripts/slurm/submit_m3_dual_domain_eval.sh`: submits augmentation off/on dual-domain TFLite evaluation. It supports grouped matrix rows per Slurm array task so the full comparison can fit under the QOS submit cap.
- `scripts/slurm/submit_m3_rotation_v2_train.sh`: submits the v2 full-dataset ablation using a gentler bounded rotation policy while keeping a clean no-augmentation v2 baseline.
- `scripts/slurm/submit_m3_rotation_v2_dual_eval.sh`: submits the v2 dual-domain eval matrix with isolated v2 artifact roots and aggregate output directory.
- `scripts/slurm/submit_m3_rotation_v3_train.sh`: submits the v3 target-orientation run using Arduino EDA gravity clusters as training-time rotation targets.
- `scripts/slurm/submit_m3_rotation_v3_dual_eval.sh`: submits the v3 dual-domain eval matrix, comparing v3 target-orientation artifacts against the clean no-augmentation v2 baseline.
- `scripts/slurm/auto_submit_m3_dual_domain_eval.sh`: optional headroom-aware autosubmitter for environments where a detached queue watcher is preferred.
- `notebooks/m3_deepconvlstm.ipynb`, `notebooks/m3_architecture_sweeps.ipynb`, plus per-experiment notebooks `notebooks/m3_E*.ipynb`.
- `reports/m3/`: consolidated M3 reports, domain-gap summary, final deployment summary, and live-trial templates.

Architecture-sweep safety additions:

- `src/m3/run_experiment.py` accepts `--model-variant` and `--run-id` overrides, so the same M3 config can run another registered architecture without copying the YAML.
- `src/m3/run_experiment.py` also accepts repeated `--model-kwarg KEY=VALUE` overrides for small architecture-specific settings.
- `--artifact-suffix` supports `{experiment_id}`, `{experiment_code}`, `{model_variant}`, and `{run_id}` placeholders.
- `scripts/slurm/submit_m3_arch_experiment.sh` submits architecture runs with a default isolated suffix of `arch_sweeps/<model_variant>/<experiment_code>`.
- `scripts/slurm/submit_m3_arch_experiment.sh` injects `patch_size=10` for XTinyHAR E08 T50 runs, because the default `patch_size=20` does not divide T50.
- This keeps non-DeepConvLSTM reports and TFLites out of the existing DeepConvLSTM `full_eXX` folders.
- Generated `reports/m3/arch_sweeps/` and `models_tflite/m3/*/arch_sweeps/` folders are ignored by Git. They remain available in the workspace for viewing, but are reproducible Slurm outputs rather than source files.

XTinyHAR compatibility additions:

- The default `xtinyhar_student_conv2d` path remains GELU, matching `notebooks/replication_xtinyhar.ipynb`.
- The XTinyHAR replication notebook and reports show FP32/PTQ/QAT TFLite export/evaluation, but the TFLM deploy gate fails for GELU. The recorded unsupported ops are `GELU` and, in the T200 replication path, `REDUCE_PROD`.
- A separate `xtinyhar_student_conv2d_relu` variant was added for TFLM compatibility testing. This is not a silent replacement for the GELU replication model.

Current staged deployment headers:

- `deploy/common/model_data.h`
- `deploy/common/model_data.cc`
- `deploy/common/norm_stats.h`

These were regenerated from an earlier DeepConvLSTM E09 PTQ INT8 pass and E09 Arduino fine-tune train-split normalization stats using Slurm job `7197`. Before the next live trial, regenerate them from the selected Daghero or DeepConvLSTM candidate below so `model_data.*` and `norm_stats.h` match.

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

Architecture-wrapper validation:

- `scripts/slurm/submit_m3_arch_experiment.sh` passes shell syntax validation.
- Slurm dry-run submissions `7201` and `7202` were canceled because GPU nodes stayed in `CONFIGURING`; this was scheduler/node behavior before the batch payload ran, not a code failure.
- Slurm dry-run submission `7204` completed with exit `0:0`, validating `daghero_cnn_2layer_conv2d` config overrides and the isolated `arch_sweeps/daghero_cnn_2layer_conv2d/e00` artifact suffix.

All-architecture smoke tests:

- Smoke jobs `7205`-`7213`: `deepconv_lstm_conv2d`, all 9 runnable configs completed `0:0`.
- Smoke jobs `7214`-`7222`: `daghero_cnn_2layer_conv2d`, all 9 runnable configs completed `0:0`.
- Smoke jobs `7225`-`7233`: `repmobile_folded_conv2d`, all 9 runnable configs completed `0:0`.
- Smoke jobs `7234`-`7242`: `tcn_attention_har_teacher_conv2d`, all 9 runnable configs completed `0:0`.
- Smoke jobs `7243`-`7251`: `tcn_inception_conv2d`, all 9 runnable configs completed `0:0`.
- Smoke jobs `7273`-`7281`: default-GELU `xtinyhar_student_conv2d`, all 9 runnable configs completed `0:0`; 9 rows exported FP32/PTQ/QAT TFLites but marked PTQ/QAT deploy gate failed because TFLM does not support GELU in our current resolver path.
- Smoke jobs `7283`-`7291`: `xtinyhar_student_conv2d_relu`, all 9 runnable configs completed `0:0`; 9 rows report FP32/PTQ/QAT deploy gate ok.

All-architecture full runs:

| Model variant | Jobs | Report rows | FP32/PTQ/QAT deploy ok | Expected deploy failures |
| --- | --- | ---: | ---: | ---: |
| `deepconv_lstm_conv2d` | `7292`-`7300` | 9 | 9 | 0 |
| `daghero_cnn_2layer_conv2d` | `7301`-`7309` | 9 | 9 | 0 |
| `repmobile_folded_conv2d` | `7310`-`7318` | 9 | 9 | 0 |
| `tcn_attention_har_teacher_conv2d` | `7319`-`7327` | 9 | 9 | 0 |
| `tcn_inception_conv2d` | `7328`-`7336` | 9 | 9 | 0 |
| `xtinyhar_student_conv2d` | `7338`-`7346` | 9 | 0 | 9 |
| `xtinyhar_student_conv2d_relu` | `7347`-`7355` | 9 | 9 | 0 |

All 63 full-run Slurm jobs completed with exit `0:0`. E01 user-holdout and E02 true-100-Hz runs were not submitted.

Accelerometer-rotation ablation reruns:

- Historical Slurm job `7497` completed with exit `0:0`, and historical dual-domain eval jobs `7606` and `7624` completed with exit `0:0`.
- On 2026-05-03, those generated ablation/eval artifacts were intentionally deleted for a clean-slate rerun with no checkpoint reuse or continued training.
- The clean rerun uses [scripts/slurm/submit_m3_rotation_ablation_train.sh](/shared/b00088568/github/har-mcu/scripts/slurm/submit_m3_rotation_ablation_train.sh), which submits four array tasks: augmentation off/on times DeepConvLSTM/Daghero.
- Clean training Slurm array job `7641` completed on 2026-05-04 with all four array tasks `COMPLETED 0:0`. No child hit the 96-hour wallclock limit; elapsed times were 15-28 minutes.
- Each array task loops over E00, E03, E04, E05, E06, E07, E08, E09, E10, E11, and E12 with `--full-dataset`.
- Augmentation-on outputs are isolated under `accel_rotation/<model_variant>/<experiment_code>/`.
- Augmentation-off outputs are isolated under `no_accel_rotation/<model_variant>/<experiment_code>/`.
- The completed training shape is 44 model/config/augmentation bundles and 132 TFLite exports: FP32, PTQ INT8, and QAT INT8 for every bundle. Every training row reports `deploy_gate_status=ptq=ok;qat=ok` and notes contain `fp32_tflite=ok`, `ptq=ok`, and `qat=ok`.

Dual-domain augmentation off/on evaluation:

- [scripts/slurm/submit_m3_dual_domain_eval.sh](/shared/b00088568/github/har-mcu/scripts/slurm/submit_m3_dual_domain_eval.sh) builds the 44-row eval matrix from the clean `accel_rotation` and `no_accel_rotation` artifact roots.
- The eval job should be submitted with `M3_SLURM_DEPENDENCY=afterok:<TRAIN_ARRAY_JOBID>` so it starts only after clean training succeeds.
- Clean eval Slurm array job `7647` completed on 2026-05-04 with all eleven array tasks `COMPLETED 0:0`. No child hit the 8-hour wallclock limit; elapsed times were under 5 minutes. Earlier dependent eval job `7646` was canceled before execution because the off-artifact suffix default was malformed; [scripts/slurm/submit_m3_dual_domain_eval.sh](/shared/b00088568/github/har-mcu/scripts/slurm/submit_m3_dual_domain_eval.sh) now builds the default suffix without shell-brace expansion.
- Each eval matrix row evaluates FP32, PTQ INT8, and QAT INT8 TFLite exports on both WISDM and Arduino test splits.
- Completed final result shape: 44 per-run CSVs and 264 master rows: 44 `{experiment, model, augmentation off/on}` combinations times 2 eval domains times 3 tiers. Every per-run CSV has exactly six rows, no aggregate rows point at missing model/norm-stats/processed paths, and no smoke paths appear in the master.
- Aggregate outputs:
  - `reports/m3/dual_domain_eval/dual_domain_eval_master.csv`
  - `reports/m3/dual_domain_eval/dual_domain_eval_master.md`
  - `reports/m3/dual_domain_eval/rotation_ablation_summary.csv`
  - `reports/m3/dual_domain_eval/rotation_ablation_summary.md`

Mean clean ablation result across E00/E03-E12:

| Model | Tier | Eval domain | Off acc | On acc | Delta acc | Off macro-F1 | On macro-F1 | Delta macro-F1 |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `daghero_cnn_2layer_conv2d` | FP32 | WISDM | 0.7636 | 0.7348 | -0.0288 | 0.7077 | 0.6445 | -0.0632 |
| `daghero_cnn_2layer_conv2d` | FP32 | Arduino | 0.5286 | 0.5241 | -0.0045 | 0.4641 | 0.4695 | +0.0053 |
| `daghero_cnn_2layer_conv2d` | PTQ | WISDM | 0.7511 | 0.7349 | -0.0162 | 0.6815 | 0.6453 | -0.0361 |
| `daghero_cnn_2layer_conv2d` | PTQ | Arduino | 0.5274 | 0.5411 | +0.0137 | 0.4628 | 0.4851 | +0.0223 |
| `daghero_cnn_2layer_conv2d` | QAT | WISDM | 0.7505 | 0.7376 | -0.0129 | 0.6796 | 0.6499 | -0.0297 |
| `daghero_cnn_2layer_conv2d` | QAT | Arduino | 0.5286 | 0.5331 | +0.0045 | 0.4636 | 0.4732 | +0.0096 |
| `deepconv_lstm_conv2d` | FP32 | WISDM | 0.7398 | 0.7188 | -0.0210 | 0.6715 | 0.6106 | -0.0609 |
| `deepconv_lstm_conv2d` | FP32 | Arduino | 0.5425 | 0.5170 | -0.0255 | 0.4971 | 0.4577 | -0.0394 |
| `deepconv_lstm_conv2d` | PTQ | WISDM | 0.7386 | 0.7187 | -0.0199 | 0.6675 | 0.6100 | -0.0575 |
| `deepconv_lstm_conv2d` | PTQ | Arduino | 0.5361 | 0.5164 | -0.0197 | 0.4941 | 0.4606 | -0.0335 |
| `deepconv_lstm_conv2d` | QAT | WISDM | 0.7004 | 0.4606 | -0.2398 | 0.6127 | 0.3198 | -0.2929 |
| `deepconv_lstm_conv2d` | QAT | Arduino | 0.4495 | 0.3057 | -0.1439 | 0.4018 | 0.2439 | -0.1579 |

Interpretation: with probability `0.5` and unconstrained uniform SO(3), the augmentation does not produce a broad win in this clean run. It slightly helps Daghero on Arduino macro-F1 for FP32/PTQ/QAT, with the clearest gain in PTQ, but reduces WISDM scores and hurts DeepConvLSTM, especially QAT. Treat this as evidence that fully uniform rotations may be too strong for the current labels/distribution; the next experiment should try a smaller orientation perturbation or lower probability rather than adopting this setting as the final deployment default.

Rotation v2 ablation:

- The v2 code path is intentionally separate from the completed `accel_rotation` and `no_accel_rotation` roots.
- Augmentation off artifacts will use `no_accel_rotation_v2/<model_variant>/<experiment_code>/`.
- Augmentation on artifacts will use `accel_rotation_v2_bounded20_p025/<model_variant>/<experiment_code>/`.
- The v2 on-policy is `mode=bounded_so3`, `probability=0.25`, `max_angle_degrees=20`, and `apply_in_qat=true`.
- `bounded_so3` samples a random 3D axis and a random angle in `[-max_angle_degrees, +max_angle_degrees]`, then applies the resulting axis-angle rotation as one shared matrix per training window.
- This is still train-only and still uses the same denormalize, rotate-in-raw-units, re-normalize path as v1. It does not change model shape, TFLite conversion, PTQ representative data, validation/test arrays, inference preprocessing, or Arduino firmware. Because `apply_in_qat=true`, v2 QAT fine-tuning batches are augmented with the same bounded-rotation policy.
- Slurm submitters:
  - `scripts/slurm/submit_m3_rotation_v2_train.sh`
  - `scripts/slurm/submit_m3_rotation_v2_dual_eval.sh`
- Submitted on 2026-05-04:
  - Training Slurm array job `7694`, with four array tasks for augmentation off/on times DeepConvLSTM/Daghero. Initial queue placement used four different GPU nodes.
  - Dependent dual-domain eval Slurm array job `7698`, with dependency `afterok:7694`, 44 matrix rows grouped as 11 array tasks.
- Completed on 2026-05-04:
  - Training job `7694`: all four array tasks `COMPLETED 0:0`, elapsed 18-27 minutes, no wallclock failures.
  - Eval job `7698`: all eleven array tasks `COMPLETED 0:0`, elapsed under 5 minutes, no wallclock failures.
  - Queue was empty after completion. Log scan found no `Traceback`, `Exception`, `FAILED`, `CANCELLED`, `TIMEOUT`, `FileNotFound`, or missing-TFLite errors; stderr content is TensorFlow runtime warnings/noise.
- Completed v2 final result shape: 44 per-run CSVs and 264 master rows, matching the v1 comparison shape.
- V2 aggregate outputs:
  - `reports/m3/dual_domain_eval_v2_bounded20_p025/dual_domain_eval_master.csv`
  - `reports/m3/dual_domain_eval_v2_bounded20_p025/dual_domain_eval_master.md`
  - `reports/m3/dual_domain_eval_v2_bounded20_p025/rotation_ablation_summary.csv`
  - `reports/m3/dual_domain_eval_v2_bounded20_p025/rotation_ablation_summary.md`
  - `reports/m3/dual_domain_eval_v2_bounded20_p025/arduino_failure_focus_delta.csv`
  - `reports/m3/dual_domain_eval_v2_bounded20_p025/arduino_failure_focus_delta.md`
  - `reports/m3/dual_domain_eval_v2_bounded20_p025/arduino_failure_focus_deployment_subset_delta.csv`
  - `reports/m3/dual_domain_eval_v2_bounded20_p025/arduino_failure_focus_deployment_subset_delta.md`

Mean v2 ablation result across E00/E03-E12:

| Model | Tier | Eval domain | Off acc | On acc | Delta acc | Off macro-F1 | On macro-F1 | Delta macro-F1 |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `daghero_cnn_2layer_conv2d` | FP32 | Arduino | 0.5286 | 0.5387 | +0.0101 | 0.4643 | 0.4775 | +0.0132 |
| `daghero_cnn_2layer_conv2d` | FP32 | WISDM | 0.7626 | 0.7629 | +0.0003 | 0.7099 | 0.7069 | -0.0030 |
| `daghero_cnn_2layer_conv2d` | PTQ | Arduino | 0.5269 | 0.5402 | +0.0133 | 0.4623 | 0.4745 | +0.0123 |
| `daghero_cnn_2layer_conv2d` | PTQ | WISDM | 0.7503 | 0.7472 | -0.0031 | 0.6777 | 0.6760 | -0.0017 |
| `daghero_cnn_2layer_conv2d` | QAT | Arduino | 0.5283 | 0.5317 | +0.0034 | 0.4630 | 0.4700 | +0.0071 |
| `daghero_cnn_2layer_conv2d` | QAT | WISDM | 0.7523 | 0.7488 | -0.0035 | 0.6873 | 0.6812 | -0.0061 |
| `deepconv_lstm_conv2d` | FP32 | Arduino | 0.5350 | 0.5219 | -0.0130 | 0.4890 | 0.4700 | -0.0189 |
| `deepconv_lstm_conv2d` | FP32 | WISDM | 0.7416 | 0.7282 | -0.0134 | 0.6756 | 0.6396 | -0.0360 |
| `deepconv_lstm_conv2d` | PTQ | Arduino | 0.5325 | 0.5212 | -0.0113 | 0.4874 | 0.4694 | -0.0180 |
| `deepconv_lstm_conv2d` | PTQ | WISDM | 0.7380 | 0.7312 | -0.0068 | 0.6687 | 0.6444 | -0.0243 |
| `deepconv_lstm_conv2d` | QAT | Arduino | 0.4726 | 0.4509 | -0.0217 | 0.4276 | 0.3997 | -0.0279 |
| `deepconv_lstm_conv2d` | QAT | WISDM | 0.6899 | 0.7105 | +0.0206 | 0.6048 | 0.6163 | +0.0115 |

V2 interpretation: `bounded_so3,20deg,p=0.25` is still only a small offline change, but the latest live deployment pass changed the recommendation. Daghero E09 v2 QAT is now the best overall on-device candidate: walking, jogging, sitting, and standing are reasonably stable in informal live tests, upstairs usually works, downstairs often gets pulled into upstairs with low confidence, and some transition windows spill into walking. DeepConvLSTM v2 improved standing versus the earlier no-augmentation live pass, but walking still often drifts to upstairs.

Deployment read from the stored test set versus live behavior: offline, the no-augmentation Daghero E09/E10 PTQ/QAT rows still tie or slightly lead the augmented rows. Live, however, Daghero E09 v2 QAT behaves better and is therefore the practical deployment recommendation. Treat the clean no-augmentation Daghero E09 QAT export as the control and rollback artifact, not as the main live target.

Rotation v3 target-orientation run:

- Purpose: test an EDA-informed orientation intervention instead of another random-rotation sweep. E04 EDA showed WISDM walking/stairs/standing mostly `+y`, Arduino walking/jogging/stairs mostly `-x`, Arduino standing split `-x/-y`, and Arduino sitting `+z`.
- V3 policy:
  - `mode=target_gravity`
  - `probability=0.25`
  - `target_vectors=[[-1,0,0],[0,-1,0],[0,0,1]]`
  - `target_probabilities=[0.50,0.25,0.25]`
  - `apply_in_qat=true`
- Mechanism: for each selected training window, denormalize to raw accelerometer units, estimate the window mean vector as a gravity/pose proxy, choose one target cluster, compute one valid rotation matrix that maps the mean vector direction toward that cluster, rotate the entire raw `[T,3]` window, and re-normalize with the same train-split mean/std. Because `apply_in_qat=true`, v3 QAT fine-tuning batches use this same target-gravity augmentation.
- This preserves per-timestep vector norms, uses exactly three accelerometer channels, and changes neither inference preprocessing nor model I/O shape.
- V3 trains only augmentation-on artifacts. Its off condition reuses the clean no-augmentation v2 baseline under `no_accel_rotation_v2/<model_variant>/<experiment_code>/`.
- V3 artifact roots:
  - `models_tflite/m3/<experiment_id>/accel_rotation_v3_target_clusters_p025/<model_variant>/<experiment_code>/`
  - `reports/m3/accel_rotation_v3_target_clusters_p025/<model_variant>/<experiment_code>/`
  - `reports/m3/dual_domain_eval_v3_target_clusters_p025/`
- Submitted on 2026-05-04:
  - Training Slurm array job `7714`, with two array tasks for DeepConvLSTM and Daghero augmentation-on training.
  - Dependent dual-domain eval Slurm array job `7716`, with dependency `afterok:7714`, 44 matrix rows grouped as 11 array tasks. The off rows reuse `no_accel_rotation_v2`.
- Completed on 2026-05-04:
  - Training job `7714`: both array tasks `COMPLETED 0:0`, elapsed 17-29 minutes, no wallclock failures.
  - Eval job `7716`: all eleven array tasks `COMPLETED 0:0`, elapsed under 5 minutes, no wallclock failures.
  - Queue was empty after completion. Log scan found no `Traceback`, `Exception`, `FAILED`, `CANCELLED`, `TIMEOUT`, `FileNotFound`, or missing-TFLite errors; stderr content is TensorFlow runtime warnings/noise.
  - Completed v3 result shape: 44 per-run CSVs, 264 master rows, and 66 v3 augmentation-on TFLite exports.
- V3 aggregate outputs:
  - `reports/m3/dual_domain_eval_v3_target_clusters_p025/dual_domain_eval_master.csv`
  - `reports/m3/dual_domain_eval_v3_target_clusters_p025/dual_domain_eval_master.md`
  - `reports/m3/dual_domain_eval_v3_target_clusters_p025/rotation_ablation_summary.csv`
  - `reports/m3/dual_domain_eval_v3_target_clusters_p025/rotation_ablation_summary.md`
  - `reports/m3/dual_domain_eval_v3_target_clusters_p025/arduino_failure_focus_delta.csv`
  - `reports/m3/dual_domain_eval_v3_target_clusters_p025/arduino_failure_focus_delta.md`
  - `reports/m3/dual_domain_eval_v3_target_clusters_p025/arduino_failure_focus_deployment_subset_delta.csv`
  - `reports/m3/dual_domain_eval_v3_target_clusters_p025/arduino_failure_focus_deployment_subset_delta.md`
  - `reports/m3/dual_domain_eval_v3_target_clusters_p025/rotation_strategy_recommendation.md`

Mean v3 ablation result across E00/E03-E12:

| Model | Tier | Eval domain | Off acc | On acc | Delta acc | Off macro-F1 | On macro-F1 | Delta macro-F1 |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `daghero_cnn_2layer_conv2d` | FP32 | Arduino | 0.5286 | 0.5281 | -0.0005 | 0.4643 | 0.4635 | -0.0008 |
| `daghero_cnn_2layer_conv2d` | FP32 | WISDM | 0.7626 | 0.7457 | -0.0169 | 0.7099 | 0.6630 | -0.0469 |
| `daghero_cnn_2layer_conv2d` | PTQ | Arduino | 0.5269 | 0.5255 | -0.0014 | 0.4623 | 0.4624 | +0.0001 |
| `daghero_cnn_2layer_conv2d` | PTQ | WISDM | 0.7503 | 0.7433 | -0.0070 | 0.6777 | 0.6608 | -0.0169 |
| `daghero_cnn_2layer_conv2d` | QAT | Arduino | 0.5283 | 0.5370 | +0.0087 | 0.4630 | 0.4768 | +0.0139 |
| `daghero_cnn_2layer_conv2d` | QAT | WISDM | 0.7523 | 0.7421 | -0.0102 | 0.6873 | 0.6567 | -0.0306 |
| `deepconv_lstm_conv2d` | FP32 | Arduino | 0.5350 | 0.5236 | -0.0113 | 0.4890 | 0.4569 | -0.0321 |
| `deepconv_lstm_conv2d` | FP32 | WISDM | 0.7416 | 0.7363 | -0.0053 | 0.6756 | 0.6505 | -0.0250 |
| `deepconv_lstm_conv2d` | PTQ | Arduino | 0.5325 | 0.5217 | -0.0109 | 0.4874 | 0.4555 | -0.0319 |
| `deepconv_lstm_conv2d` | PTQ | WISDM | 0.7380 | 0.7358 | -0.0021 | 0.6687 | 0.6488 | -0.0199 |
| `deepconv_lstm_conv2d` | QAT | Arduino | 0.4726 | 0.4291 | -0.0435 | 0.4276 | 0.3773 | -0.0504 |
| `deepconv_lstm_conv2d` | QAT | WISDM | 0.6899 | 0.6681 | -0.0218 | 0.6048 | 0.5680 | -0.0368 |

V3 interpretation: target-gravity rotation did not become the new deployment default. It gives a mean Arduino gain for Daghero QAT, but it hurts WISDM and does not beat the no-augmentation Daghero baseline in the deployment-relevant E09-E12 subset. It also hurts DeepConvLSTM across FP32/PTQ/QAT mean Arduino metrics, and DeepConvLSTM remains too large relative to Daghero for the first on-device candidate. The useful conclusion is that the EDA-informed target rotation is a better hypothesis than blind rotation, but the stored dataset still does not reproduce the live failure strongly enough to select an augmented model from offline metrics alone.

Experiment ladder and what we learned:

| Run | Purpose | Policy | What we achieved | Decision |
| --- | --- | --- | --- | --- |
| v1 | Stress-test whether physically valid arbitrary orientation changes help. | `uniform_so3`, `p=0.5`, `apply_in_qat=true` | Proved the shared train-only augmentation path works for FP32, fine-tune, and QAT with no inference cost. Found unconstrained rotations are too blunt: Daghero Arduino improves slightly, DeepConvLSTM especially QAT gets hurt. | Keep as reference, not deployment default. |
| v2 | Test a gentler random perturbation after v1 was too strong. | `bounded_so3`, `20deg`, `p=0.25`, `apply_in_qat=true` | Reduced damage compared with v1 and gave Daghero small mean Arduino gains. Stored Arduino standing/walking are already near-perfect for Daghero E09/E10, but informal live testing favored this branch. | Use Daghero E09 v2 QAT as the main live deployment branch; keep the clean model as rollback. |
| v3 | Use observed WISDM-vs-Arduino axis/domain shift instead of blind random rotations. | `target_gravity`, targets `-x/-y/+z`, `p=0.25`, `apply_in_qat=true` | Completed. It directly rotates WISDM-like gravity directions toward Arduino clusters and works technically, but the offline metrics do not beat v2 as the live deployment choice. | Keep as EDA-informed reference, not the main live deployment branch. |

QAT augmentation rule and recommendation:

- In code, [src/quant/qat_train.py](/shared/b00088568/github/har-mcu/src/quant/qat_train.py) calls `build_training_input(..., for_qat=True)`. [src/train/augment.py](/shared/b00088568/github/har-mcu/src/train/augment.py) then honors `augment.accel_rotation.apply_in_qat`.
- In v1, v2, and v3, `apply_in_qat=true`, so augmented QAT exports were trained with the same rotation policy as the corresponding FP32/fine-tune training stage.
- If `apply_in_qat=false`, QAT training uses unaugmented normalized `X_train`, even when earlier FP32/fine-tune training used augmentation. Validation/test arrays and PTQ representative data remain unaugmented either way.
- For future controlled augmentation experiments, keep `apply_in_qat=true` so QAT does not see a different training distribution from FP32/fine-tune. The current live recommendation is already Daghero E09 v2 QAT, but keep the no-augmentation Daghero E09 QAT export as the control and rollback comparison.

Deployment guideline right now:

- The main live deployment target is Daghero E09 v2 QAT under `accel_rotation_v2_bounded20_p025`, not the no-augmentation baseline.
- Keep the no-augmentation Daghero E09 QAT artifact as the control and rollback model.
- Main live candidate, Daghero QAT INT8:
  - Model: `models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/accel_rotation_v2_bounded20_p025/daghero_cnn_2layer_conv2d/e09/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E09_daghero_cnn_2layer_conv2d_r0_qat.tflite`
  - Norm stats: `data/processed/m3/E09_wisdm_pretrain_arduino_finetune/accel_rotation_v2_bounded20_p025/daghero_cnn_2layer_conv2d/e09/finetune_arduino/norm_stats_T100_Prandom_stratified.json`
  - Live note: walking, jogging, sitting, and standing are fairly stable; upstairs is usually correct; downstairs often flips to upstairs with low confidence.
- Backup candidate if QAT has any on-device issue, Daghero PTQ INT8:
  - Model: `models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/accel_rotation_v2_bounded20_p025/daghero_cnn_2layer_conv2d/e09/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E09_daghero_cnn_2layer_conv2d_r0_ptq_int8.tflite`
  - Same fine-tune Arduino norm stats as above.
- Offline control / rollback candidate, Daghero QAT INT8 with no augmentation:
  - Model: `models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/no_accel_rotation_v2/daghero_cnn_2layer_conv2d/e09/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E09_daghero_cnn_2layer_conv2d_r0_qat.tflite`
  - Same experiment, same train split, no augmentation.
- DeepConvLSTM comparison candidate, PTQ INT8:
  - Model: `models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e09/deepconv_lstm_conv2d_T100_Prandom_stratified_E09_deepconv_lstm_r0_ptq_int8.tflite`
  - Norm stats: `data/processed/m3/E09_wisdm_pretrain_arduino_finetune/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e09/finetune_arduino/norm_stats_T100_Prandom_stratified.json`
  - Live note: standing improved compared with the older no-augmentation live pass, but walking still often drifts into upstairs.
- T50 follow-up target set:
  - Train and evaluate E08, E11, and E12 with v2 bounded rotation for both Daghero and DeepConvLSTM, then compare FP32/PTQ/QAT on both WISDM and Arduino.
  - Submitted on 2026-05-04 as training Slurm job `7758` with dependent dual-domain eval job `7759`.
  - Completion check: all `7758_*` and `7759_*` tasks finished `COMPLETED` with exit code `0:0`. Log review found no tracebacks, missing-file errors, cancellations, or timeouts; stderr content was limited to TensorFlow runtime noise and one matplotlib legend warning.
  - Aggregate-only step is complete for `reports/m3/dual_domain_eval_v2_bounded20_p025_t50/`. The generated `dual_domain_eval_master.csv` and `dual_domain_eval_master.md` summarize 72 rows from 12 source CSVs.
  - That aggregate confirms full T50 evaluation coverage for E08, E11, and E12 across augmentation on/off, Daghero and DeepConvLSTM, both WISDM and Arduino test sets, and FP32/PTQ/QAT exports.
- Pretraining-ablation target set:
  - Deploy E10 on-device to test whether WISDM pretraining plus Arduino fine-tuning is actually necessary, or whether training directly on device IMU data is sufficient.
  - Treat E12 as the T50 from-scratch analogue of E10. In other words, the requested "E10 with augmentations at T=50" experiment is already represented by E12.
- On-device test priority: verify the actual live confusion behavior for `Standing`, `Walking`, `Upstairs`, and `Downstairs`, and explicitly log confidence so low-confidence and high-confidence failures can be separated.
- We still need a systematic pocket-orientation sweep; the next logged live run should cover board-in-hand, left-pocket, and alternate pocket orientation placements.
- After the main E09 live pass, the next scientific deployment comparison should be E10 Daghero v2 QAT. That is the direct test of whether pretraining is helping or whether a from-scratch device-only model is good enough.
- Use E12 Daghero v2 QAT as the matching T50 from-scratch comparison.
- Export commands for the first candidate:

```bash
/shared/b00088568/myenvs/tinymlproj/bin/python -m src.deploy.export_c_array \
  --tflite models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/accel_rotation_v2_bounded20_p025/daghero_cnn_2layer_conv2d/e09/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E09_daghero_cnn_2layer_conv2d_r0_qat.tflite \
  --out-dir deploy/common

/shared/b00088568/myenvs/tinymlproj/bin/python -m src.deploy.export_norm_header \
  --norm-json data/processed/m3/E09_wisdm_pretrain_arduino_finetune/accel_rotation_v2_bounded20_p025/daghero_cnn_2layer_conv2d/e09/finetune_arduino/norm_stats_T100_Prandom_stratified.json \
  --out deploy/common/norm_stats.h
```

Team update summary:

- Goal: improve Arduino Nano 33 BLE Sense HAR robustness to orientation changes without adding gyro/magnetometer channels, changing model shapes, or adding inference-time cost.
- Done: built a shared train-only accelerometer rotation path used by FP32/source-only/from-scratch, fine-tune, and QAT training; validation/test/PTQ representative data stay untouched.
- Done: ran clean full-dataset v1, v2, and v3 DeepConvLSTM/Daghero experiments and dual-domain WISDM/Arduino TFLite evaluation for FP32, PTQ, and QAT.
- Done: added EDA showing a real axis/domain shift: WISDM mostly `+y`, Arduino dynamic activities mostly `-x`, Arduino standing `-x/-y`, Arduino sitting `+z`.
- Finding: arbitrary `uniform_so3,p=0.5` is too strong; bounded `20deg,p=0.25` is the current best live policy even though the offline delta is small; target-gravity v3 remains a reference branch rather than the main deployment choice.
- Current best deployable reference for live use: Daghero E09 v2 QAT, about `26.7 KB`, with better live robustness than the clean baseline.
- M4 report alignment: `paper/M4.tex` now treats Daghero E09 v2 QAT as the final deployment candidate, the clean Daghero E09 QAT artifact as the control/rollback model, and DeepConvLSTM E09 v2 PTQ as the architecture comparison.
- Left to do: export the selected Daghero candidate into `deploy/common`, run the logged live robustness sweep, compare E09 against E10 on-device to test whether pretraining is necessary, and collect failure windows for the DeepConvLSTM deep dive.

## M4 Published Reference Comparison And Deployment Notes

`paper/M4.tex` now includes a published-reference comparison table so the final report does not only compare our models against our own previous milestones.

Reference numbers used in M4:

| System | Published/current result | Footprint/latency note | How to interpret it |
| --- | --- | --- | --- |
| Original DeepConvLSTM, Ordonez and Roggen 2016 | OPPORTUNITY F1 `0.930/0.895` for locomotion and `0.866/0.915` for gestures depending on null-class setting; Skoda F1 `0.958` | No Nano/TFLite size or latency reported | Historical source of the CNN+LSTM architecture, but not directly comparable to our accelerometer-only WISDM/Arduino TinyML setting. |
| Published DeepConv LSTM edge reference, Zhou et al. 2025 | WISDM accuracy `98.24%`, F1 `98.23%`; quantized model about `97%` accuracy/F1 | Size `513.23 KB -> 136.51 KB`; Arduino Nano 33 BLE Sense Rev2 Edge Impulse deployment reported `29.1 KB` RAM, `189.6 KB` flash, `21 ms` average inference | Closest WISDM/edge DeepConvLSTM reference for our project. |
| Our DeepConvLSTM E00 source anchor | WISDM FP32 `97.83%` accuracy / `96.82%` macro-F1; PTQ `97.88%` / `96.93%` | `513.617 KB` FP32, `136.922 KB` PTQ; our local TFLM LSTM path is too slow live | Similar source-domain scale, but not the deployment choice. |
| Published Daghero CNN, Daghero et al. 2022 | WISDM max F1 `98.9%`; Max-5% point F1 `94.74%` | Max point `6.22 KB`, `4.19 ms`; Max-5% point `1.27 KB`, `1.07 ms` on Quentin RISC-V | Motivates the lightweight CNN path; their mixed/sub-byte backend is not directly comparable to TFLite flatbuffer size. |
| Our Daghero E00 source anchor | WISDM v2 QAT `99.41%` accuracy / `99.18%` macro-F1 | `26.734 KB` TFLite flatbuffer | Confirms our Daghero implementation is a strong WISDM classifier. |
| Our final Daghero E09 v2 deployment branch | Arduino held-out `99.56%` accuracy / `99.56%` macro-F1; stored-test Walking and Standing recall `1.0` | `26.734 KB` flatbuffer; mean live `Invoke()` about `68.6 ms` | Final live candidate because it gives the best size, latency, stored-test, and current live-behavior balance. |

The comparison is intentionally not presented as a strict leaderboard. Zhou et al. used an Edge Impulse deployment stack on Nano 33 BLE Sense Rev2; Daghero et al. used mixed/sub-byte quantization on the Quentin RISC-V MCU. Our numbers are TensorFlow Lite flatbuffer sizes and local TensorFlow Lite Micro behavior on our Nano 33 BLE Sense sketch.

M4 diagram alignment:

- The Markdown Mermaid pipeline in `docs/m3_end_to_end_pipeline.md` is represented as TikZ in `paper/M4.tex`.
- M4 includes TikZ diagrams for the full training/evaluation/deployment pipeline, train-time rotation augmentation, and Arduino deployment.
- The augmentation diagram explicitly shows `normalized train window -> denormalize -> rotate raw [T,3] -> re-normalize -> model.fit/QAT fit`, with validation/test/PTQ representative data bypassing augmentation.

Arduino deployment specificity:

- Current sketch: `deploy/m3_nano_int8_ble_imu/m3_nano_int8_ble_imu.ino`.
- Current v2 model header include: `daghero_accel_rotation_v2_bounded20_p025_qat.h`.
- Current normalization header include for T100: `m3_norm_finetune_t100.h`.
- Core live settings: `M3_KWINDOW_SIZE=100`, hop `50`, `LIVE_SAMPLE_RATE_HZ=100`, and `kAccelScaleDivisor=4.0f` before z-score normalization.
- Firmware path: LSM9DS1 accel sample, scale, z-score normalize with exported stats, quantize into INT8 tensor, call TFLM `Invoke()`, print/notify prediction, confidence, timing, and confusion counts.
- BLE commands: START/STOP, average, set/clear ground truth. Serial remains the detailed debug/evidence channel.
- No augmentation, no gyro/magnetometer features, and no orientation correction run on-device.

## Orientation Failure Notes And Next Strategy

The on-device problem we actually care about is not abstract benchmark accuracy. The Arduino Nano 33 BLE Sense sometimes predicts true `Standing` as `Walking`, and sometimes true `Walking` as `Downstairs` or `Upstairs`. Those are examples of the failures we noticed, not the complete failure set. The next evaluation pass should therefore track full Arduino-domain confusion matrices, per-class recall, and the named standing/walking/stairs confusion pairs instead of relying only on mean accuracy or macro-F1.

Paper traceability:

- Yurtman and Barshan 2017, "Activity Recognition Invariant to Sensor Orientation with Wearable Motion Sensors" (`https://doi.org/10.3390/s17081838`), motivates the problem framing: wearable HAR pipelines are brittle when a device is placed at a different orientation. From this paper we take the experimental priority of orientation robustness and the idea that a 3-axis motion vector should be treated geometrically under rotations. We do not copy their full orientation-invariant preprocessing path because this repo must keep the current accelerometer-only model and on-device preprocessing contract.
- Yurtman, Barshan, and Fidan 2018, "Activity Recognition Invariant to Wearable Sensor Unit Orientation Using Differential Rotational Transformations Represented by Quaternions" (`https://doi.org/10.3390/s18082725`), is the cautionary source. It motivates orientation-invariant transformations, but it also sits in a richer wearable-motion-sensor setting where gyroscope/magnetometer information can support orientation reasoning. From this paper we take the caution not to claim true Earth-frame correction from our accelerometer-only setup and not to add gyro or magnetometer channels in this change.
- Caramaschi, Papini, and Caiani 2023, "Device Orientation Independent Human Activity Recognition Model for Patient Monitoring Based on Triaxial Acceleration" (`https://doi.org/10.3390/app13074175`), is the direct augmentation precedent. They rotate triaxial accelerometer signals with rotation matrices to make a single-accelerometer HAR model more robust to device displacement. From this paper we take the train-time rotation idea, the requirement that the rotation be physically meaningful in raw acceleration space, and the caution that large rotations can damage walking-like classes because gravity-aligned components carry label information. That caution is why v1 `uniform_so3,p=0.5` is now a reference result rather than the deployment default, and why v2 uses bounded rotations.

Current EDA snapshot:

- New EDA command:

```bash
/shared/b00088568/myenvs/tinymlproj/bin/python -m src.m3.axis_eda \
  --config configs/m3/E04_wisdm_to_g_arduino_g.yaml \
  --output-dir reports/m3/axis_eda/e04_g_units
```

- EDA outputs:
  - `reports/m3/axis_eda/e04_g_units/axis_eda_report.md`
  - `reports/m3/axis_eda/e04_g_units/sample_axis_summary.csv`
  - `reports/m3/axis_eda/e04_g_units/window_axis_summary.csv`
  - `reports/m3/axis_eda/e04_g_units/dominant_axis_summary.csv`
- Under E04's unit-compatible view, WISDM is converted to g and Arduino raw readings are rescaled by the firmware factor of `4.0`.
- WISDM `Walking`, `Upstairs`, `Downstairs`, and `Standing` windows are mostly gravity-dominant on `+y`; WISDM `Sitting` is mostly `+z`.
- Arduino `Walking` is `-x` dominant for 100% of windows, Arduino `Jogging` is mostly `-x`, Arduino `Sitting` is `+z`, and Arduino `Standing` splits almost exactly between `-x` and `-y`.
- Arduino `Standing` dynamic RMS is `0.0118`, much lower than WISDM `Standing` at `0.0466` and far below WISDM/Arduino walking-like classes. That means the stored Arduino test-set `Standing` windows are static; the live Standing-to-Walking failure is likely tied to a live orientation/posture/sampling/normalization condition not fully represented by the held-out Arduino CSV.
- Arduino `Upstairs` and `Downstairs` dynamic RMS are higher than WISDM (`+0.2205` and `+0.1527` respectively), while Arduino `Walking` is slightly lower than WISDM. This supports the observed walking/stairs confusion: these dynamic classes overlap in energy and are also axis-shifted.

Recommended next experiment strategy:

1. Do not adopt `probability=0.5`, `mode=uniform_so3` as the deployment default. Keep the completed run as a reference negative/partial-positive result.
2. Do not spend another full Slurm sweep on the bounded-rotation grid. The narrow v2 T50 follow-up for E08, E11, and E12 has completed; use it to decide whether shorter windows are worth live testing.
3. The next logged live session should include board-in-hand, left-pocket, and alternate pocket orientation trials. Log confidence values so low-confidence and high-confidence failures can be counted explicitly.
4. Treat the stored E04 axis EDA as the current orientation proxy. The important proxy facts are WISDM dynamic/static classes mostly `+y`, Arduino walking/jogging mostly `-x`, Arduino standing split `-x/-y`, and Arduino sitting `+z`.
5. Target-orientation v3 has now been run. It is technically valid and EDA-informed, but it is still not the main live deployment choice.
6. Keep the generated failure-focus reports as the decision surface:
   - `arduino_failure_focus_delta.csv`
   - `arduino_failure_focus_deployment_subset_delta.csv`
   - per-class recalls and confusion pairs for `Standing -> Walking`, `Walking -> Upstairs`, `Walking -> Downstairs`, `Upstairs -> Walking`, and `Downstairs -> Walking`
7. Keep Daghero as the leading deployment architecture unless a later run changes the stored-test and on-device picture. DeepConvLSTM v2 standing improved live, but walking still tends to move toward upstairs, so a deeper failure analysis is needed before it can replace Daghero.
8. If v2 still leaves clear live gaps after the T50 follow-up, test a mixed-magnitude rotation schedule with an explicit prior over realistic device reorientations rather than one fixed bounded angle.
9. Keep inference-time preprocessing and TFLite model shapes fixed unless we explicitly open a separate deployment-change experiment. Training-time augmentation remains the preferred path because it preserves on-device cost.

## Key Results

The aggregate report is:

- `reports/m3/m3_experiment_master.csv`
- `reports/m3/m3_experiment_master.md`

All nine full DeepConvLSTM runs exported:

- FP32 `.tflite`
- PTQ INT8 `.tflite`
- QAT INT8 `.tflite`

There are 27 full-run TFLite exports under `models_tflite/m3/`.

DeepConvLSTM full-run export pattern:

```text
models_tflite/m3/<experiment_id>/full_eXX/<model>_T<window>_Prandom_stratified_<run_id>_fp32.tflite
models_tflite/m3/<experiment_id>/full_eXX/<model>_T<window>_Prandom_stratified_<run_id>_ptq_int8.tflite
models_tflite/m3/<experiment_id>/full_eXX/<model>_T<window>_Prandom_stratified_<run_id>_qat.tflite
```

Accelerometer-rotation rerun export pattern:

```text
models_tflite/m3/<experiment_id>/accel_rotation/<model_variant>/<experiment_code>/<model>_T<window>_Prandom_stratified_<run_id>_fp32.tflite
models_tflite/m3/<experiment_id>/accel_rotation/<model_variant>/<experiment_code>/<model>_T<window>_Prandom_stratified_<run_id>_ptq_int8.tflite
models_tflite/m3/<experiment_id>/accel_rotation/<model_variant>/<experiment_code>/<model>_T<window>_Prandom_stratified_<run_id>_qat.tflite
```

No-rotation ablation rerun export pattern:

```text
models_tflite/m3/<experiment_id>/no_accel_rotation/<model_variant>/<experiment_code>/<model>_T<window>_Prandom_stratified_<run_id>_fp32.tflite
models_tflite/m3/<experiment_id>/no_accel_rotation/<model_variant>/<experiment_code>/<model>_T<window>_Prandom_stratified_<run_id>_ptq_int8.tflite
models_tflite/m3/<experiment_id>/no_accel_rotation/<model_variant>/<experiment_code>/<model>_T<window>_Prandom_stratified_<run_id>_qat.tflite
```

Rotation v2 export patterns:

```text
models_tflite/m3/<experiment_id>/accel_rotation_v2_bounded20_p025/<model_variant>/<experiment_code>/<model>_T<window>_Prandom_stratified_<run_id>_fp32.tflite
models_tflite/m3/<experiment_id>/accel_rotation_v2_bounded20_p025/<model_variant>/<experiment_code>/<model>_T<window>_Prandom_stratified_<run_id>_ptq_int8.tflite
models_tflite/m3/<experiment_id>/accel_rotation_v2_bounded20_p025/<model_variant>/<experiment_code>/<model>_T<window>_Prandom_stratified_<run_id>_qat.tflite

models_tflite/m3/<experiment_id>/no_accel_rotation_v2/<model_variant>/<experiment_code>/<model>_T<window>_Prandom_stratified_<run_id>_fp32.tflite
models_tflite/m3/<experiment_id>/no_accel_rotation_v2/<model_variant>/<experiment_code>/<model>_T<window>_Prandom_stratified_<run_id>_ptq_int8.tflite
models_tflite/m3/<experiment_id>/no_accel_rotation_v2/<model_variant>/<experiment_code>/<model>_T<window>_Prandom_stratified_<run_id>_qat.tflite
```

Rotation v3 export patterns:

```text
models_tflite/m3/<experiment_id>/accel_rotation_v3_target_clusters_p025/<model_variant>/<experiment_code>/<model>_T<window>_Prandom_stratified_<run_id>_fp32.tflite
models_tflite/m3/<experiment_id>/accel_rotation_v3_target_clusters_p025/<model_variant>/<experiment_code>/<model>_T<window>_Prandom_stratified_<run_id>_ptq_int8.tflite
models_tflite/m3/<experiment_id>/accel_rotation_v3_target_clusters_p025/<model_variant>/<experiment_code>/<model>_T<window>_Prandom_stratified_<run_id>_qat.tflite
```

V1/v2/v3 TFLite artifact map:

| Run | Condition | Artifact suffix | TFLite directory pattern |
| --- | --- | --- | --- |
| v1 | Augmentation on | `accel_rotation` | `models_tflite/m3/<experiment_id>/accel_rotation/<model_variant>/<experiment_code>/` |
| v1 | Augmentation off | `no_accel_rotation` | `models_tflite/m3/<experiment_id>/no_accel_rotation/<model_variant>/<experiment_code>/` |
| v2 | Augmentation on | `accel_rotation_v2_bounded20_p025` | `models_tflite/m3/<experiment_id>/accel_rotation_v2_bounded20_p025/<model_variant>/<experiment_code>/` |
| v2 | Augmentation off | `no_accel_rotation_v2` | `models_tflite/m3/<experiment_id>/no_accel_rotation_v2/<model_variant>/<experiment_code>/` |
| v3 | Augmentation on | `accel_rotation_v3_target_clusters_p025` | `models_tflite/m3/<experiment_id>/accel_rotation_v3_target_clusters_p025/<model_variant>/<experiment_code>/` |
| v3 | Augmentation off | `no_accel_rotation_v2` | v3 reuses the clean v2 no-augmentation baseline. |

Each full suffix currently has 66 TFLite files: E00/E03/E04/E05/E06/E07/E08/E09/E10/E11/E12 times `deepconv_lstm_conv2d` and `daghero_cnn_2layer_conv2d` times FP32/PTQ/QAT. Deployment-oriented files end in `_ptq_int8.tflite` or `_qat.tflite`.

Coverage audit on 2026-05-04:

- Excluding user-holdout variants, every non-user-holdout experiment in this repo has complete v1/v2/v3 and clean coverage.
- E10 has 6 TFLites per suffix: 2 model variants times FP32/PTQ/QAT.
- E12 has the same complete 6-per-suffix coverage and is the T50 from-scratch analogue of E10.

T50 v2 augmented TFLite roots from the 2026-05-04 follow-up:

- `models_tflite/m3/E08_T50_window/accel_rotation_v2_bounded20_p025/<model_variant>/e08/`
- `models_tflite/m3/E11_wisdm_pretrain_arduino_finetune_T50/accel_rotation_v2_bounded20_p025/<model_variant>/e11/`
- `models_tflite/m3/E12_arduino_from_scratch_T50/accel_rotation_v2_bounded20_p025/<model_variant>/e12/`

Here `<model_variant>` is `daghero_cnn_2layer_conv2d` or `deepconv_lstm_conv2d`. Each directory contains FP32, PTQ INT8, and QAT INT8 TFLites. The paired clean T50 controls live under the same experiment roots with `no_accel_rotation_v2`.

Accelerometer-rotation TFLite sizes from the completed rerun:

| Model | Window | FP32 TFLite KB | PTQ INT8 KB | QAT INT8 KB |
| --- | ---: | ---: | ---: | ---: |
| `deepconv_lstm_conv2d` | 100 | 513.617 | 136.922 | 137.344 |
| `deepconv_lstm_conv2d` | 50 | 396.430 | 107.625 | 108.047 |
| `daghero_cnn_2layer_conv2d` | 100 | 80.406 | 26.133 | 26.734 |
| `daghero_cnn_2layer_conv2d` | 50 | 80.406 | 26.133 | 26.734 |

Dual-domain comparison outputs:

```text
reports/m3/dual_domain_eval/<augment_label>/<model_variant>/<experiment_code>/dual_domain_eval.csv
reports/m3/dual_domain_eval/<augment_label>/<model_variant>/<experiment_code>/dual_domain_eval.json
reports/m3/dual_domain_eval/dual_domain_eval_master.csv
reports/m3/dual_domain_eval/dual_domain_eval_master.md
```

T50 v2 follow-up aggregate outputs:

```text
reports/m3/dual_domain_eval_v2_bounded20_p025_t50/<augment_label>/<model_variant>/<experiment_code>/dual_domain_eval.csv
reports/m3/dual_domain_eval_v2_bounded20_p025_t50/dual_domain_eval_master.csv
reports/m3/dual_domain_eval_v2_bounded20_p025_t50/dual_domain_eval_master.md
reports/m3/dual_domain_eval_v2_bounded20_p025_t50/job_matrix.tsv
```

The master table records `model_path`, `normalization_stats`, `processed_dir`, `accuracy`, `macro_f1`, `model_size_kb`, `input_dtype`, and `output_dtype` for every FP32/PTQ/QAT evaluation on WISDM and Arduino.

Example deployment candidate exports:

```text
models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/full_e09/deepconv_lstm_conv2d_T100_Prandom_stratified_E09_deepconv_lstm_r0_fp32.tflite
models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/full_e09/deepconv_lstm_conv2d_T100_Prandom_stratified_E09_deepconv_lstm_r0_ptq_int8.tflite
models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/full_e09/deepconv_lstm_conv2d_T100_Prandom_stratified_E09_deepconv_lstm_r0_qat.tflite
```

Current staged DeepConvLSTM deployment candidate:

- Experiment: `E09_wisdm_pretrain_arduino_finetune`
- Candidate export: PTQ INT8
- FP32 accuracy / macro-F1: `0.995575221238938` / `0.9955735520260941`
- PTQ accuracy / macro-F1: `0.9879898862199747` / `0.9880066511463083`
- QAT accuracy / macro-F1: `0.9298356510745891` / `0.9298920081134151`
- Deployment summary: `reports/m3/final_deployment_summary.md`

This is the model currently exported into `deploy/common/model_data.*` from the earlier DeepConvLSTM deployment pass. It is no longer the recommended next live-test candidate. For the next on-device trial, regenerate `deploy/common/model_data.*` and `deploy/common/norm_stats.h` from the Daghero E09 no-augmentation QAT artifact listed above. E07 is diagnostic-only and must not be selected as the final deployed model.

Architecture sweep outputs:

- Full reports: 63 `m3_experiment_master.csv` files under `reports/m3/arch_sweeps/<model_variant>/<experiment_code>/`.
- Full TFLite exports: 189 `.tflite` files under `models_tflite/m3/<experiment_id>/arch_sweeps/<model_variant>/<experiment_code>/`.
- Smoke reports: 63 `m3_experiment_master.csv` files under `reports/m3/smoke_arch_sweeps/<model_variant>/<experiment_code>/`.
- Smoke TFLite exports: 189 `.tflite` files under `models_tflite/m3/<experiment_id>/smoke_arch_sweeps/<model_variant>/<experiment_code>/`.
- All non-GELU architecture variants completed with `fp32_tflite=ok; ptq=ok; qat=ok`.
- Default-GELU `xtinyhar_student_conv2d` completed conversion/evaluation but has 9 rows with `fp32_tflite=ok; ptq=failed; qat=failed` because the TFLM deploy gate rejects `GELU`.

Example full architecture-sweep export location:

```text
models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/arch_sweeps/<model_variant>/e09/
```

For an XTinyHAR deployment-compatible candidate, use the explicit ReLU variant rather than the GELU replication variant:

```text
models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/arch_sweeps/xtinyhar_student_conv2d_relu/e09/
```

E09 Arduino fine-tune quick comparison:

- Best deploy-eligible E09 macro-F1 in this sweep is `daghero_cnn_2layer_conv2d`, with PTQ macro-F1 `0.9962107846145144` and QAT macro-F1 `0.9962107846145146`.
- `tcn_inception_conv2d` is very close, with PTQ macro-F1 `0.9949398022317159` and QAT macro-F1 `0.9962036380132565`.
- Default-GELU `xtinyhar_student_conv2d` is not deploy eligible despite valid host-side TFLite evaluation because the TFLM deploy gate fails.
- Before replacing the staged DeepConvLSTM deployment headers, compare E09 accuracy, macro-F1, model size, latency, and Arduino live-trial behavior.

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

The wrappers also contain the same Slurm defaults, so if `symbolic-motifgen/scripts/aus_hpc_env.sh` is unavailable on another checkout, set the `M3_SLURM_*`, `M3_REPO_ROOT`, and `M3_CONDA_ENV` variables directly before submitting.

To run a different architecture without mixing outputs with DeepConvLSTM:

```bash
bash scripts/slurm/submit_m3_arch_experiment.sh \
  configs/m3/E00_wisdm_m2_anchor.yaml \
  daghero_cnn_2layer_conv2d
```

The architecture wrapper defaults to:

```text
reports/m3/arch_sweeps/<model_variant>/<experiment_code>/
models_tflite/m3/<experiment_id>/arch_sweeps/<model_variant>/<experiment_code>/
checkpoints/m3/<experiment_id>/arch_sweeps/<model_variant>/<experiment_code>/
data/processed/m3/<experiment_id>/arch_sweeps/<model_variant>/<experiment_code>/
```

For smoke testing another model first:

```bash
bash scripts/slurm/submit_m3_arch_experiment.sh \
  configs/m3/E00_wisdm_m2_anchor.yaml \
  daghero_cnn_2layer_conv2d \
  --smoke --max-windows-per-class 20 --representative-samples 16
```

Registered Conv2D-safe architecture variants:

- `deepconv_lstm_conv2d`
- `daghero_cnn_2layer_conv2d`
- `repmobile_folded_conv2d`
- `tcn_attention_har_teacher_conv2d`
- `tcn_inception_conv2d`
- `xtinyhar_student_conv2d`
- `xtinyhar_student_conv2d_relu`

Run the clean full-dataset DeepConvLSTM/Daghero augmentation ablation matrix:

```bash
bash scripts/slurm/submit_m3_rotation_ablation_train.sh
```

Run the dual-domain off/on TFLite comparison after the training array succeeds:

```bash
M3_SLURM_DEPENDENCY=afterok:<TRAIN_ARRAY_JOBID> \
M3_DUAL_EVAL_TASK_START=0 \
M3_DUAL_EVAL_TASK_LIMIT=44 \
M3_DUAL_EVAL_TASKS_PER_ARRAY_TASK=4 \
M3_DUAL_EVAL_ARRAY_CONCURRENCY=11 \
bash scripts/slurm/submit_m3_dual_domain_eval.sh
```

Aggregate after all chunks finish:

```bash
/shared/b00088568/myenvs/tinymlproj/bin/python -m src.m3.dual_domain_eval --aggregate-only --output-dir reports/m3/dual_domain_eval
```

Run the v2 bounded-rotation ablation:

```bash
bash scripts/slurm/submit_m3_rotation_v2_train.sh
```

Run the v2 dual-domain off/on TFLite comparison after the v2 training array succeeds:

```bash
M3_SLURM_DEPENDENCY=afterok:<TRAIN_ARRAY_JOBID> \
bash scripts/slurm/submit_m3_rotation_v2_dual_eval.sh
```

Aggregate v2 results:

```bash
/shared/b00088568/myenvs/tinymlproj/bin/python -m src.m3.dual_domain_eval --aggregate-only --output-dir reports/m3/dual_domain_eval_v2_bounded20_p025
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

The current notebooks are DeepConvLSTM-oriented. For non-DeepConvLSTM runs, prefer `scripts/slurm/submit_m3_arch_experiment.sh` or add notebook cells that call that wrapper, not the plain `full_eXX` suffix commands. This avoids mixing architecture outputs with the completed DeepConvLSTM folders.

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
| `notebooks/m3_architecture_sweeps.ipynb` | Non-DeepConvLSTM architecture sweep control notebook | Prints/submits architecture smoke runs and full matrix runs through `submit_m3_arch_experiment.sh` | `reports/m3/arch_sweeps/<model_variant>/<experiment_code>/`, `models_tflite/m3/<experiment_id>/arch_sweeps/<model_variant>/<experiment_code>/` |
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
- `tiny-motion/Arduino_layth_hamza_wisdm_raw_numeric_user.csv` and `tiny-motion/Arduino_layth_hamza_wisdm_raw.csv` have matching samples; the numeric-user file uses user `37`, while the raw file uses user `layth`.
- The first Arduino timestamps differ by `50,000,000` timestamp units, which is 50 ms if interpreted as nanoseconds, matching 20 Hz.
- The WISDM CSV also follows the WISDM-style approximately 50 ms cadence, with small timestamp jitter.
- E03, E04, E05, E06, E07, E09, and E10 run with T100 at 20 Hz.
- E08 runs T50 at 20 Hz for the 2.5-second window ablation.

What we matched:

- There is no Hz mismatch for the current merged Arduino CSVs used in the completed M3 runs; both WISDM and Arduino are operating on the 20 Hz path.
- We matched the current Arduino dataset to the WISDM-compatible 20 Hz/T100 path for the main transfer and adaptation experiments.
- We kept 50% overlap.
- We evaluated unit convention matching in E04 by converting WISDM to g and keeping Arduino in g-style units.
- We evaluated the legacy opposite convention in E05 as a negative-control style ablation.

What we did not run:

- We did not run true Arduino 100 Hz T500 because the current merged Arduino source available to the repo is already 20 Hz.
- E02 remains the config/tooling path for a future true-100-Hz Arduino source.
- We did not upsample WISDM to 100 Hz.
- We did not run E01 user-holdout experiments.

## Other Architecture Status

The architecture sweep is now complete for the runnable M3 matrix: E00 and E03-E10 for each registered Conv2D-safe architecture variant plus the explicit XTinyHAR ReLU compatibility variant. Outputs are separated by model under `reports/m3/arch_sweeps/<model_variant>/<experiment_code>/` and `models_tflite/m3/<experiment_id>/arch_sweeps/<model_variant>/<experiment_code>/`.

Summary:

- `deepconv_lstm_conv2d`, `daghero_cnn_2layer_conv2d`, `repmobile_folded_conv2d`, `tcn_attention_har_teacher_conv2d`, `tcn_inception_conv2d`, and `xtinyhar_student_conv2d_relu` all report FP32/PTQ/QAT deploy gate ok for all 9 runnable experiments.
- Default-GELU `xtinyhar_student_conv2d` matches the XTinyHAR replication notebook behavior: TFLite conversion and host evaluation run, but PTQ/QAT deploy gate fails for TFLM because of unsupported `GELU`.
- `xtinyhar_student_conv2d_relu` is the compatibility variant to use if XTinyHAR is selected for on-device deployment.
- E08 XTinyHAR runs use `patch_size=10`; non-E08 XTinyHAR runs keep the default `patch_size=20`.

## DeepConvLSTM And Daghero End-To-End Contract

The current DeepConvLSTM and Daghero M3 code path is documented in detail in `docs/m3_end_to_end_pipeline.md`. That document includes:

- raw inputs and processed array shapes;
- transfer-mode flow;
- train-time rotation behavior;
- FP32, PTQ, and QAT training and export paths;
- callbacks, loss functions, optimizers, scheduler behavior, and metrics;
- exact DeepConvLSTM and Daghero layer summaries;
- TFLite sizes for T100 and T50;
- host-side TFLite evaluation and dual-domain comparison;
- Arduino deployment header generation and live inference behavior.

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
- generated architecture-sweep reports under `reports/m3/arch_sweeps/`
- generated architecture-sweep TFLites under `models_tflite/m3/*/arch_sweeps/`

The first three exclusions were explicitly requested for this repo handoff. The generated data and executed notebook outputs are also local/reproducible artifacts and are ignored to keep the Git history lightweight.

The ablation TFLite exports under `models_tflite/m3/*/accel_rotation/` and `models_tflite/m3/*/no_accel_rotation/` are not ignored by `.gitignore`; include them in the handoff commit if the commit is meant to preserve the clean augmented/no-augmentation model exports. The dual-domain aggregate reports under `reports/m3/dual_domain_eval/` are also reproducibility outputs for the augmentation off/on comparison and should be reviewed before deciding whether to commit them.
