# M3 Rotation Experiment Team Update

## Goal

Improve HAR robustness to Arduino Nano 33 BLE Sense orientation changes without adding gyroscope or magnetometer channels, changing `[T,3]` model inputs, changing class outputs, or adding inference-time cost.

## What We Built

- A shared train-only accelerometer rotation path used by FP32/source-only/from-scratch training, Arduino fine-tuning, and QAT training.
- The augmentation denormalizes each normalized training window back to raw accelerometer units, applies one valid 3D rotation matrix to the whole `[T,3]` window, and re-normalizes with the same train-split mean/std.
- Validation, test, PTQ representative data, TFLite conversion shape, and Arduino inference code are unchanged.
- Dual-domain evaluation now compares FP32, PTQ, and QAT TFLite exports on both WISDM and Arduino test splits.
- Axis EDA now summarizes WISDM-vs-Arduino gravity direction and dynamic energy shifts.

## Experiment Ladder

| Run | Purpose | Policy | Result | Decision |
| --- | --- | --- | --- | --- |
| v1 | Test whether arbitrary physically valid orientation changes help. | `uniform_so3`, `p=0.5` | Daghero Arduino improves slightly, but WISDM drops and DeepConvLSTM QAT is hurt badly. | Reference only, not deployment default. |
| v2 | Make random rotation gentler. | `bounded_so3`, `20deg`, `p=0.25` | Safer than v1 and small mean Daghero Arduino gain, but deployment subset E09-E12 is flat/slightly worse for Daghero and worse for DeepConvLSTM QAT. | Do not run more bounded grids yet. |
| v3 | Use EDA-observed Arduino orientation clusters instead of blind random rotations. | `target_gravity`, targets `-x/-y/+z`, `p=0.25` | Completed. Daghero QAT mean Arduino improves, but WISDM drops and deployment subset does not beat no augmentation. DeepConvLSTM gets worse in mean Arduino metrics. | Do not deploy by default; stop offline rotation sweeps until live failure data is captured. |

## What We Learned

- EDA shows a real axis/domain shift: WISDM walking/stairs/standing are mostly `+y`, Arduino walking/jogging/stairs are mostly `-x`, Arduino standing splits `-x/-y`, and Arduino sitting is `+z`.
- Stored Arduino standing windows are very static, and the best Daghero E09/E10 stored-test models already have standing and walking recall of `1.0`. The stored split therefore does not reproduce the live Standing-to-Walking issue.
- Mean accuracy and macro-F1 are not enough. We now track per-class recall and standing/walking/stairs confusion pairs.
- Daghero is the current best deployment architecture to test first because its INT8 model is about `26-27 KB` while matching or beating the stored-test behavior of larger DeepConvLSTM candidates.
- V1, v2, and v3 all showed that train-time rotation is technically compatible with FP32/fine-tune/QAT and TFLite, but none of the rotation policies is strong enough to replace the no-augmentation Daghero deployment baseline from offline results.

## Deploy Now For On-Device Testing

Short version: deploy one model at a time. The first live test should use the no-augmentation Daghero E09 QAT model. The DeepConvLSTM candidate is useful as an architecture comparison, but it is larger and the best DeepConvLSTM QAT row is weaker than Daghero on the stored Arduino split.

Recommended order:

| Priority | Architecture | Tier | Experiment | Window | Augmentation | Why |
| --- | --- | --- | --- | ---: | --- | --- |
| 1 | Daghero | QAT INT8 | E09 WISDM pretrain + Arduino fine-tune | T100 | Off | Best first on-device candidate: about `26.7 KB`, stored Arduino accuracy/macro-F1 about `0.9956`, standing recall `1.0`, walking recall `1.0`. |
| 2 | Daghero | PTQ INT8 | E09 WISDM pretrain + Arduino fine-tune | T100 | Off | Backup if QAT behaves unexpectedly on-device: about `26.1 KB`, stored Arduino accuracy about `0.9937`, standing/walking recall `1.0`. |
| 3 | DeepConvLSTM | PTQ INT8 | E09 WISDM pretrain + Arduino fine-tune | T100 | Off | Best like-for-like DeepConvLSTM T100 comparison: about `136.9 KB`, stored Arduino macro-F1 about `0.9886`. |
| 4 | DeepConvLSTM | QAT INT8 | E11 WISDM pretrain + Arduino fine-tune | T50 | Off | Only if the team specifically wants a DeepConvLSTM QAT comparison: about `108.0 KB`, stored Arduino macro-F1 about `0.9664`. |

Primary Daghero QAT candidate:

```text
models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/no_accel_rotation_v2/daghero_cnn_2layer_conv2d/e09/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E09_daghero_cnn_2layer_conv2d_r0_qat.tflite
data/processed/m3/E09_wisdm_pretrain_arduino_finetune/no_accel_rotation_v2/daghero_cnn_2layer_conv2d/e09/finetune_arduino/norm_stats_T100_Prandom_stratified.json
```

Daghero PTQ backup:

```text
models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/no_accel_rotation_v2/daghero_cnn_2layer_conv2d/e09/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E09_daghero_cnn_2layer_conv2d_r0_ptq_int8.tflite
data/processed/m3/E09_wisdm_pretrain_arduino_finetune/no_accel_rotation_v2/daghero_cnn_2layer_conv2d/e09/finetune_arduino/norm_stats_T100_Prandom_stratified.json
```

DeepConvLSTM PTQ comparison:

```text
models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/no_accel_rotation_v2/deepconv_lstm_conv2d/e09/deepconv_lstm_conv2d_T100_Prandom_stratified_E09_deepconv_lstm_r0_ptq_int8.tflite
data/processed/m3/E09_wisdm_pretrain_arduino_finetune/no_accel_rotation_v2/deepconv_lstm_conv2d/e09/finetune_arduino/norm_stats_T100_Prandom_stratified.json
```

DeepConvLSTM QAT comparison, only if QAT is required for this architecture:

```text
models_tflite/m3/E11_wisdm_pretrain_arduino_finetune_T50/no_accel_rotation_v2/deepconv_lstm_conv2d/e11/deepconv_lstm_conv2d_T50_Prandom_stratified_E11_deepconv_lstm_r0_qat.tflite
data/processed/m3/E11_wisdm_pretrain_arduino_finetune_T50/no_accel_rotation_v2/deepconv_lstm_conv2d/e11/finetune_arduino/norm_stats_T50_Prandom_stratified.json
```

These recommended artifacts are all `no_accel_rotation_v2`, meaning no train-time rotation augmentation was used for them. The v1/v2/v3 rotation-augmented artifacts remain valid experiment outputs, but they are not the deployment default because the offline dual-domain results did not beat the no-augmentation Daghero deployment baseline.

## If We Want To Test An Augmented Model

The augmented branch should be treated as a controlled on-device comparison after the no-augmentation Daghero QAT baseline. Do not replace the baseline with an augmented model unless live trials show a clear improvement on the failure cases.

Recommended augmented order:

| Priority | Architecture | Run | Tier | Experiment | Policy | Stored Arduino summary |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Daghero | v2 | QAT INT8 | E09 | `bounded_so3`, `20deg`, `p=0.25` | Best augmented candidate: accuracy/macro-F1 about `0.9956`, standing/walking recall `1.0`, size about `26.7 KB`. |
| 2 | Daghero | v3 | QAT INT8 | E09 | `target_gravity`, `p=0.25`, targets `-x/-y/+z` | Best EDA-informed augmented candidate: accuracy/macro-F1 about `0.9949`, standing/walking recall `1.0`, size about `26.7 KB`. |
| 3 | Daghero | v1 | QAT INT8 | E09 | `uniform_so3`, `p=0.5` | Stress-test reference only: accuracy/macro-F1 about `0.9867`; too much offline damage to deploy by default. |
| 4 | DeepConvLSTM | v2 | PTQ INT8 | E09 | `bounded_so3`, `20deg`, `p=0.25` | Best augmented DeepConvLSTM comparison: macro-F1 about `0.9855`, size about `136.9 KB`; still not better than Daghero. |

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
- Validation and test data are never augmented. PTQ representative data is never augmented.
- On-device normalization uses the exported `norm_stats.h` constants. The Arduino sketch scales raw IMU samples, applies the same z-score normalization when `APPLY_NORMALIZATION=1`, quantizes into the model input tensor, and invokes TFLM.
- No augmentation runs on the Arduino. There is zero inference-time rotation cost.

## Next Steps

1. Export the no-augmentation E09 Daghero QAT candidate to `deploy/common/model_data.*` and `deploy/common/norm_stats.h`.
2. Flash the Nano 33 BLE Sense and run live standing/walking/stairs trials.
3. If QAT behaves unexpectedly on-device, repeat with the matching E09 Daghero PTQ artifact.
4. If the no-augmentation QAT baseline still shows orientation-like failures, export the v2 Daghero QAT augmented candidate and run the same live protocol.
5. If the team wants an EDA-informed augmented comparison, export the v3 Daghero QAT candidate after v2.
6. If the team wants an architecture comparison, export the E09 DeepConvLSTM PTQ candidate and run the same live script and trial protocol.
7. Record raw windows and predictions for failures, especially true `Standing`, `Walking`, `Upstairs`, and `Downstairs`, but keep the full confusion matrix because those are examples rather than the only failure modes.
8. Use those live failure windows to decide whether the problem is orientation, sampling cadence, normalization scale, ring-buffer behavior, or an activity/posture gap not represented by the stored Arduino CSV.
9. Do not run more rotation sweeps until live failure data shows what axis/energy condition needs to be targeted.

## Message To Share

I tried three training-time accelerometer rotation strategies to make the HAR model less sensitive to Nano 33 BLE Sense orientation while keeping the device code and model shape unchanged. The augmentation pipeline works and is compatible with FP32, fine-tuning, QAT, PTQ/TFLite export, and dual-domain evaluation. However, the offline results do not justify deploying a rotation-augmented model as the default. The first practical on-device candidate is the small Daghero E09 no-augmentation QAT model; the matching PTQ model is the backup. If we want an augmented comparison, the best one to test is Daghero E09 v2 QAT with bounded 20-degree rotations at `p=0.25`; the EDA-informed v3 Daghero QAT model is the next augmented comparison. For a DeepConvLSTM comparison, use the E09 no-augmentation PTQ model, or v2 DeepConvLSTM PTQ if the comparison specifically needs an augmented DeepConvLSTM. Normalization is still required on-device through the matching `norm_stats.h`, and no augmentation runs on-device.
