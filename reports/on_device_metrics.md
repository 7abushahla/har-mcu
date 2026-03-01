# On-Device Metrics

This report is populated after running Arduino deployment benchmarks.

## Required fields
- Board: Arduino Nano 33 BLE Sense
- Model: PTQ INT8 `.tflite`
- Flash usage (KB)
- Tensor arena / RAM usage (KB)
- `Invoke()` latency (ms)
- End-to-end latency (buffering + invoke, ms)
- Power (mW) and energy per inference (optional)

## Reproduction steps
1. Export model array:
   - `python -m src.deploy.export_c_array --tflite <model.tflite> --out-dir deploy/common`
2. Export normalization header:
   - `python -m src.deploy.export_norm_header --norm-json <norm_stats.json> --out deploy/common/norm_stats.h`
3. Build and upload `deploy/arduino_infer/arduino_infer.ino`.
4. Capture serial output and compile memory summary.
5. Copy metrics into this report.
