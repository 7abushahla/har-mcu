# M3 Rotation Experiment Team Update

## Goal

Improve HAR robustness to Arduino Nano 33 BLE Sense orientation changes without adding gyroscope or magnetometer channels, changing `[T,3]` model inputs, changing class outputs, or adding inference-time cost.

## What We Built

- A shared train-only accelerometer rotation path used by FP32/source-only/from-scratch training, Arduino fine-tuning, and QAT training.
- The augmentation denormalizes each normalized training window back to raw accelerometer units, applies one valid 3D rotation matrix to the whole `[T,3]` window, and re-normalizes with the same train-split mean/std.
- Validation, test, PTQ representative data, TFLite conversion shape, and Arduino inference code are unchanged.
- Dual-domain evaluation now compares FP32, PTQ, and QAT TFLite exports on both WISDM and Arduino test splits.
- Axis EDA now summarizes WISDM-vs-Arduino gravity direction and dynamic energy shifts.
- QAT uses the same training-input builder as FP32 and fine-tuning. In v1, v2, and v3, `apply_in_qat: true`, so QAT fine-tuning batches are augmented with the same active rotation policy. PTQ calibration/representative data is not augmented.

## Experiment Ladder

| Run | Purpose | Policy | Result | Decision |
| --- | --- | --- | --- | --- |
| v1 | Test whether arbitrary physically valid orientation changes help. | `uniform_so3`, `p=0.5` | Daghero Arduino improves slightly, but WISDM drops and DeepConvLSTM QAT is hurt badly. | Reference only, not deployment default. |
| v2 | Make random rotation gentler. | `bounded_so3`, `20deg`, `p=0.25` | Offline mean F1 is slightly weaker than the clean baseline, but informal live trials improved the actual on-device behavior enough that Daghero E09 v2 QAT is now the main deployment candidate. DeepConvLSTM standing improved, but walking still often drifts to upstairs. | Promote Daghero v2 QAT for live testing; run a narrow T50 follow-up instead of another full sweep. |
| v3 | Use EDA-observed Arduino orientation clusters instead of blind random rotations. | `target_gravity`, targets `-x/-y/+z`, `p=0.25` | Completed. Daghero QAT mean Arduino improves, but WISDM drops and the live E09 v2 Daghero result is still the cleaner deployment choice. DeepConvLSTM gets worse in mean Arduino metrics. | Keep as reference, not the main live deployment candidate. |

## What We Learned

- EDA shows a real axis/domain shift: WISDM walking/stairs/standing are mostly `+y`, Arduino walking/jogging/stairs are mostly `-x`, Arduino standing splits `-x/-y`, and Arduino sitting is `+z`.
- Stored Arduino standing windows are very static, and the best offline Daghero E09/E10 rows already have standing and walking recall of `1.0`. The stored split therefore still under-represents the live failure modes.
- Mean accuracy and macro-F1 are not enough. The latest live pass showed that v2 bounded rotation can lose a little offline F1 yet still improve actual deployment behavior.
- Daghero is still the strongest deployment architecture because its INT8 model is about `26-27 KB` and its live behavior is better than DeepConvLSTM under the current augmentation settings.
- Current live best overall candidate: Daghero E09 v2 QAT under `accel_rotation_v2_bounded20_p025`. In informal testing it handled walking, jogging, sitting, and standing fairly well.
- The main live Daghero v2 failure pattern was low-confidence ambiguity, not repeated high-confidence lock-in. Upstairs generally worked well, while downstairs often flipped to upstairs with low confidence; some transition windows also fell to walking.
- DeepConvLSTM v2 improved standing compared with the earlier no-augmentation live pass, but walking still usually drifted to upstairs, so it remains the weaker live deployment choice.
- We have not yet completed a logged robustness sweep for board-in-hand, left-pocket, and alternate pocket orientations. Tomorrow's live session should include those placements and record confidence values so failures can be counted instead of described qualitatively.

## Deploy Now For On-Device Testing

Short version: for live deployment, start with the augmented branch. The current best overall on-device candidate is Daghero E09 v2 QAT under `accel_rotation_v2_bounded20_p025`. Keep the no-augmentation Daghero E09 QAT model as the offline control and rollback option.

Recommended order:

| Priority | Architecture | Tier | Experiment | Window | Augmentation | Why |
| --- | --- | --- | --- | ---: | --- | --- |
| 1 | Daghero | QAT INT8 | E09 WISDM pretrain + Arduino fine-tune | T100 | v2 on | Current best overall live candidate: about `26.7 KB`; walking, jogging, sitting, and standing are stable in informal live testing; upstairs usually works; downstairs often flips to upstairs with low confidence. |
| 2 | Daghero | PTQ INT8 | E09 WISDM pretrain + Arduino fine-tune | T100 | v2 on | Quantized fallback if the QAT export behaves unexpectedly on-device; same augmentation policy and small footprint. |
| 3 | Daghero | QAT INT8 | E09 WISDM pretrain + Arduino fine-tune | T100 | v2 off | Offline control and rollback candidate. Use this if tomorrow's live run does not reproduce the augmented advantage. |
| 4 | DeepConvLSTM | PTQ INT8 | E09 WISDM pretrain + Arduino fine-tune | T100 | v2 on | Architecture comparison only. Standing improved relative to the old no-augmentation live pass, but walking still tends to drift to upstairs. |

Primary Daghero QAT candidate:

```text
models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/accel_rotation_v2_bounded20_p025/daghero_cnn_2layer_conv2d/e09/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E09_daghero_cnn_2layer_conv2d_r0_qat.tflite
data/processed/m3/E09_wisdm_pretrain_arduino_finetune/accel_rotation_v2_bounded20_p025/daghero_cnn_2layer_conv2d/e09/finetune_arduino/norm_stats_T100_Prandom_stratified.json
```

Daghero PTQ backup:

```text
models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/accel_rotation_v2_bounded20_p025/daghero_cnn_2layer_conv2d/e09/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E09_daghero_cnn_2layer_conv2d_r0_ptq_int8.tflite
data/processed/m3/E09_wisdm_pretrain_arduino_finetune/accel_rotation_v2_bounded20_p025/daghero_cnn_2layer_conv2d/e09/finetune_arduino/norm_stats_T100_Prandom_stratified.json
```

Daghero no-augmentation control:

```text
models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/no_accel_rotation_v2/daghero_cnn_2layer_conv2d/e09/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E09_daghero_cnn_2layer_conv2d_r0_qat.tflite
data/processed/m3/E09_wisdm_pretrain_arduino_finetune/no_accel_rotation_v2/daghero_cnn_2layer_conv2d/e09/finetune_arduino/norm_stats_T100_Prandom_stratified.json
```

DeepConvLSTM PTQ comparison:

```text
models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e09/deepconv_lstm_conv2d_T100_Prandom_stratified_E09_deepconv_lstm_r0_ptq_int8.tflite
data/processed/m3/E09_wisdm_pretrain_arduino_finetune/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e09/finetune_arduino/norm_stats_T100_Prandom_stratified.json
```

Why the live recommendation changed:

- Offline dual-domain scores still slightly favor the clean baseline, but the live deployment behavior improved with v2 bounded rotation, which is the decision signal that matters most here.
- Most observed Daghero v2 failures were low-confidence ambiguities rather than repeated high-confidence wrong labels. That is a better failure mode for the next round of debugging because it suggests uncertainty near orientation or transition boundaries rather than a consistent wrong attractor.
- The downstairs-to-upstairs confusion appears asymmetric. Upstairs looked good live, but some of that apparent success may be inflated because downstairs often gets pulled upward with low confidence.
- Because some misclassifications happen between steps or during transitions, a shorter T50 window is worth checking before designing a more complex augmentation schedule.

Submitted T50 v2 follow-up on 2026-05-04:

- Training Slurm array job `7758` for E08, E11, and E12 under v2 bounded rotation, covering both Daghero and DeepConvLSTM plus the paired clean controls.
- Dependent dual-domain eval Slurm job `7759`, writing its matrix under `reports/m3/dual_domain_eval_v2_bounded20_p025_t50/`.
- Completion check: all `7758_*` and `7759_*` tasks finished `COMPLETED` with exit code `0:0`. Log review found no tracebacks, missing-artifact errors, cancellations, or timeouts. Stderr content was limited to expected TensorFlow converter/runtime noise and one matplotlib legend warning.
- Aggregate-only step is now complete. `reports/m3/dual_domain_eval_v2_bounded20_p025_t50/dual_domain_eval_master.csv` and `.md` summarize 72 evaluation rows from 12 source CSVs.
- That master table confirms full T50 coverage for E08, E11, and E12 across augmentation on/off, Daghero and DeepConvLSTM, both WISDM and Arduino test sets, and FP32/PTQ/QAT exports.

## Where The V1/V2/V3 TFLites Live

All v1/v2/v3 M3 TFLite exports follow this pattern:

```text
models_tflite/m3/<experiment_id>/<artifact_suffix>/<model_variant>/<experiment_code>/<model_file>.tflite
```

Each full suffix below currently has 66 TFLite files: 11 experiments times 2 model variants times FP32/PTQ/QAT.

| Run | Condition | Artifact suffix | TFLite directory pattern |
| --- | --- | --- | --- |
| v1 | Augmentation on | `accel_rotation` | `models_tflite/m3/<experiment_id>/accel_rotation/<model_variant>/<experiment_code>/` |
| v1 | Augmentation off | `no_accel_rotation` | `models_tflite/m3/<experiment_id>/no_accel_rotation/<model_variant>/<experiment_code>/` |
| v2 | Augmentation on | `accel_rotation_v2_bounded20_p025` | `models_tflite/m3/<experiment_id>/accel_rotation_v2_bounded20_p025/<model_variant>/<experiment_code>/` |
| v2 | Augmentation off | `no_accel_rotation_v2` | `models_tflite/m3/<experiment_id>/no_accel_rotation_v2/<model_variant>/<experiment_code>/` |
| v3 | Augmentation on | `accel_rotation_v3_target_clusters_p025` | `models_tflite/m3/<experiment_id>/accel_rotation_v3_target_clusters_p025/<model_variant>/<experiment_code>/` |
| v3 | Augmentation off | `no_accel_rotation_v2` | v3 reuses the clean v2 no-augmentation baseline. |

The model variants used for this rotation comparison are:

- `daghero_cnn_2layer_conv2d`
- `deepconv_lstm_conv2d`

The deployable INT8 files end in:

- `_ptq_int8.tflite`
- `_qat.tflite`

Coverage audit on 2026-05-04:

- Excluding user-holdout variants, every non-user-holdout experiment in this repo has complete v1/v2/v3 coverage: `E00`, `E03`, `E04`, `E05`, `E06`, `E07`, `E08`, `E09`, `E10`, `E11`, and `E12`.
- Each experiment contributes 6 TFLites per suffix: 2 model variants times FP32/PTQ/QAT.
- E10 has complete v1/v2/v3 and clean bundles under `models_tflite/m3/E10_arduino_from_scratch/...`.
- The T50 from-scratch analogue of E10 is E12, and it also has complete v1/v2/v3 and clean bundles under `models_tflite/m3/E12_arduino_from_scratch_T50/...`.

New T50 v2 augmented TFLites from this follow-up are under:

- `models_tflite/m3/E08_T50_window/accel_rotation_v2_bounded20_p025/<model_variant>/e08/`
- `models_tflite/m3/E11_wisdm_pretrain_arduino_finetune_T50/accel_rotation_v2_bounded20_p025/<model_variant>/e11/`
- `models_tflite/m3/E12_arduino_from_scratch_T50/accel_rotation_v2_bounded20_p025/<model_variant>/e12/`

Here `<model_variant>` is `daghero_cnn_2layer_conv2d` or `deepconv_lstm_conv2d`, and each directory contains FP32, PTQ INT8, and QAT INT8 exports. The paired clean T50 controls live under the same experiment roots with `no_accel_rotation_v2` instead of `accel_rotation_v2_bounded20_p025`.

## If We Want To Test An Augmented Model

The augmented branch is now the main live branch. The no-augmentation Daghero E09 QAT artifact remains the control and rollback option, while Daghero v2 QAT is the main deployment target.

Recommended augmented order:

| Priority | Architecture | Run | Tier | Experiment | Policy | Stored Arduino summary |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Daghero | v2 | QAT INT8 | E09 | `bounded_so3`, `20deg`, `p=0.25` | Current best live model: stable walking/jogging/sitting/standing, good upstairs, weak downstairs, small footprint. |
| 2 | Daghero | v2 | PTQ INT8 | E09 | `bounded_so3`, `20deg`, `p=0.25` | Fallback if QAT is unstable on-device. |
| 3 | Daghero | v3 | QAT INT8 | E09 | `target_gravity`, `p=0.25`, targets `-x/-y/+z` | EDA-informed alternative if v2 still struggles after tomorrow's live pass. |
| 4 | DeepConvLSTM | v2 | PTQ INT8 | E09 | `bounded_so3`, `20deg`, `p=0.25` | Architecture comparison only; standing is better than before, but walking still tends to move toward upstairs. |

V2 Daghero QAT augmented candidate:

```text
models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/accel_rotation_v2_bounded20_p025/daghero_cnn_2layer_conv2d/e09/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E09_daghero_cnn_2layer_conv2d_r0_qat.tflite
data/processed/m3/E09_wisdm_pretrain_arduino_finetune/accel_rotation_v2_bounded20_p025/daghero_cnn_2layer_conv2d/e09/finetune_arduino/norm_stats_T100_Prandom_stratified.json
```

V3 Daghero QAT augmented candidate:

```text
models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/accel_rotation_v3_target_clusters_p025/daghero_cnn_2layer_conv2d/e09/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E09_daghero_cnn_2layer_conv2d_r0_qat.tflite
data/processed/m3/E09_wisdm_pretrain_arduino_finetune/accel_rotation_v3_target_clusters_p025/daghero_cnn_2layer_conv2d/e09/finetune_arduino/norm_stats_T100_Prandom_stratified.json
```

V1 Daghero QAT augmented reference:

```text
models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/accel_rotation/daghero_cnn_2layer_conv2d/e09/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E09_daghero_cnn_2layer_conv2d_r0_qat.tflite
data/processed/m3/E09_wisdm_pretrain_arduino_finetune/accel_rotation/daghero_cnn_2layer_conv2d/e09/finetune_arduino/norm_stats_T100_Prandom_stratified.json
```

V2 DeepConvLSTM PTQ augmented comparison:

```text
models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e09/deepconv_lstm_conv2d_T100_Prandom_stratified_E09_deepconv_lstm_r0_ptq_int8.tflite
data/processed/m3/E09_wisdm_pretrain_arduino_finetune/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e09/finetune_arduino/norm_stats_T100_Prandom_stratified.json
```

Normalization and augmentation explanation:

- Dataset normalization fits `mean` and `std` only on the relevant training split, then applies those stats to train/validation/test arrays.
- For E09 and E11 fine-tune deployments, use the `finetune_arduino/norm_stats_*.json` file because the final model is adapted on the Arduino fine-tune train split.
- Rotation augmentation, when enabled in v1/v2/v3, is train-only. It denormalizes each selected training window to raw accelerometer units, rotates the raw `[T,3]` window with one valid 3D rotation, and re-normalizes with the same train-split stats.
- QAT is included in that train-only rule. For augmented v1/v2/v3 runs, QAT training also sees augmented batches because `augment.accel_rotation.apply_in_qat` is `true`. If that key is set to `false`, QAT receives the unaugmented normalized `X_train` arrays even when FP32/fine-tune training used augmentation.
- Validation and test data are never augmented. PTQ representative data is never augmented.
- On-device normalization uses the exported `norm_stats.h` constants. The Arduino sketch scales raw IMU samples, applies the same z-score normalization when `APPLY_NORMALIZATION=1`, quantizes into the model input tensor, and invokes TFLM.
- No augmentation runs on the Arduino. There is zero inference-time rotation cost.

Recommendation on QAT augmentation:

- Keep `apply_in_qat: true` for any future controlled augmentation ablation so FP32/fine-tune training and QAT fine-tuning see the same training distribution.
- The current primary live deployment candidate is Daghero E09 v2 QAT, but keep the no-augmentation Daghero E09 QAT export as the control and rollback model.
- Treat the v2 Daghero QAT recommendation as a live-deployment conclusion, not as proof that offline macro-F1 should dominate model selection.

## Next Steps

1. Export the Daghero E09 v2 QAT candidate to `deploy/common/model_data.*` and `deploy/common/norm_stats.h`.
2. Keep the no-augmentation Daghero E09 QAT export ready as the control and rollback comparison.
3. Run tomorrow's live session with board-in-hand, left-pocket, and alternate pocket orientations, and log the serial confidence stream so low-confidence and high-confidence failures can be counted.
4. Run the narrow T50 v2 follow-up for E08, E11, and E12 on both Daghero and DeepConvLSTM, then evaluate FP32/PTQ/QAT on both WISDM and Arduino.
5. Check whether T50 reduces downstairs-to-upstairs confusion and transition-window spillover into walking.
6. Write up a deeper DeepConvLSTM failure analysis focused on orientation sensitivity, walking-versus-stairs confusion, and quantization sensitivity under augmented training.
7. If v2 still leaves clear live failure pockets, test a mixed-magnitude augmentation schedule with an explicit prior over realistic device reorientations instead of one fixed bounded angle.
8. Extend live evaluation to continuous streams that include transitions such as sitting to standing, standing to walking, walking to jogging, and walking to upstairs.
9. Deploy E10 on-device as the direct pretraining ablation. This is the cleanest way to test whether WISDM pretraining plus Arduino fine-tuning is actually necessary, or whether training only on the device IMU data is sufficient.
10. Treat E12 as the T50 version of that same question. E10 is the T100 from-scratch run, while E12 is the T50 from-scratch run.

Recommended pretraining-ablation artifacts:

- E10 Daghero v2 QAT (from-scratch, T100): `models_tflite/m3/E10_arduino_from_scratch/accel_rotation_v2_bounded20_p025/daghero_cnn_2layer_conv2d/e10/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E10_daghero_cnn_2layer_conv2d_r0_qat.tflite`
- Matching norm stats: `data/processed/m3/E10_arduino_from_scratch/accel_rotation_v2_bounded20_p025/daghero_cnn_2layer_conv2d/e10/norm_stats_T100_Prandom_stratified.json`
- E12 Daghero v2 QAT (from-scratch, T50): `models_tflite/m3/E12_arduino_from_scratch_T50/accel_rotation_v2_bounded20_p025/daghero_cnn_2layer_conv2d/e12/daghero_cnn_2layer_conv2d_T50_Prandom_stratified_E12_daghero_cnn_2layer_conv2d_r0_qat.tflite`
- Matching norm stats: `data/processed/m3/E12_arduino_from_scratch_T50/accel_rotation_v2_bounded20_p025/daghero_cnn_2layer_conv2d/e12/norm_stats_T50_Prandom_stratified.json`

## Message To Share

I tried three training-time accelerometer rotation strategies to make the HAR model less sensitive to Nano 33 BLE Sense orientation while keeping the device code and model shape unchanged. The augmentation pipeline works and is compatible with FP32, fine-tuning, QAT, PTQ/TFLite export, and dual-domain evaluation. Offline macro-F1 still slightly favors the clean baseline, but the latest live deployment behavior shifted the recommendation: the current best overall on-device model is Daghero E09 v2 QAT with bounded 20-degree rotation augmentation at `p=0.25`. It handles walking, jogging, sitting, and standing fairly well in informal live trials, while upstairs is usually correct and downstairs is the main weak class, often with low-confidence confusion into upstairs. DeepConvLSTM v2 fixed standing relative to the earlier no-augmentation live pass, but walking still tends to drift to upstairs, so it remains the comparison model rather than the main deployment choice. The next step is a narrow T50 v2 follow-up for Daghero and DeepConvLSTM plus a logged live session that captures confidence, pocket placement, and activity transitions. Normalization is still required on-device through the matching `norm_stats.h`, and no augmentation runs on-device.
