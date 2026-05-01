# M3 Live Trial Protocol

Use this protocol after a final non-diagnostic model has been exported to `deploy/common/`.

## Before Flashing

- Confirm the selected experiment is not diagnostic-only.
- Confirm `deploy/common/model_data.h` and `deploy/common/model_data.cc` were generated from the selected `.tflite`.
- Confirm `deploy/common/norm_stats.h` was generated from the selected `norm_stats.json`.
- Confirm the Arduino sketch uses the same `WINDOW_SIZE`, sample rate, unit mode, and normalization convention as training.

## Slurm Reproduction

Submit training/export work from the host node only through Slurm wrappers:

```bash
source symbolic-motifgen/scripts/aus_hpc_env.sh
bash scripts/slurm/submit_m3_experiment.sh configs/m3/E00_wisdm_m2_anchor.yaml
```

Inside jobs, activate:

```bash
conda activate /shared/b00088568/myenvs/tinymlproj
```

Do not run host-node Python for training, evaluation, data loading, schema inspection, quantization, or TFLite evaluation.

## Arduino Trial

1. Flash `deploy/arduino_infer/arduino_infer.ino` after regenerating deployment headers.
2. Open serial logging at `115200` baud.
3. Record at least 50 inference rows per tested activity.
4. Save rows using `reports/m3/live_trial_template.csv` as the schema.
5. Record any dropped samples, unusual board orientation, cable motion, reset, or serial interruption in `notes`.

Expected serial row format:

```text
timestamp_ms,label,confidence,invoke_ms,e2e_ms
```

The sketch should also print `tensor_arena_bytes` during setup and average invoke latency after at least 50 inferences.
