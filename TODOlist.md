# TODOlist.md - Implementation Status

## Completed
- [x] Phase 0: Repo scaffold and config files.
- [x] Conda environment packaging files and docs added (`environment.yml`, `requirements.txt`, README setup steps for `tinymlproj`).
- [x] Phase 1: Deterministic data pipeline (cleaning, windowing, split protocols, train-only normalization).
- [x] Phase 2: Baseline DeepConv+LSTM training/eval scripts.
- [x] Phase 3: Window sweep pipeline.
- [x] Phase 4: PTQ full-int8 export + TFLite evaluation scripts.
- [x] Phase 5: QAT best-effort export with fallback notes.
- [x] Phase 6: Deploy utilities (C-array export, norm export, TFLM op check) + Arduino sketches.
- [x] Phase 7: TinyOL simulator + Arduino TinyOL scaffold.
- [x] Phase 8: `src/run_all.py` orchestration and final table generation.
- [x] Phase 9: Smoke runner + tests scaffold.
- [x] Phase 10: Shared JSON serialization hardening across training/eval/quant/smoke/deploy reports.
- [x] Added regression tests for NumPy/TensorFlow scalar JSON payloads and fixed split test fixture sizing for modern scikit-learn constraints.
- [x] Phase 11: Strict full-int8 PTQ policy for Nano 33 BLE Sense replication (no mixed fallback), with notebook strict-gate guardrails and PTQ status/error schema.
- [x] Phase 12: Dual-track PTQ/QAT replication in TF 2.14.1 (paper-metric reporting + strict Nano deployability), including calibration variants (`traincal`, `authorcal`) and strict dual gate enforcement in smoke/run_all.

## Implemented Files
- `configs/default.yaml`, `configs/smoke.yaml`
- `pyproject.toml`, `requirements.lock.txt`
- `environment.yml`, `requirements.txt`
- `scripts/env/check_tf_cuda.py`, `scripts/env/check_versions.py`
- `src/data/*.py`, `src/models/*.py`, `src/train/*.py`, `src/eval/*.py`
- `src/sweeps/window_size_sweep.py`
- `src/quant/ptq_full_int8.py`, `src/quant/qat_train.py`
- `src/deploy/export_c_array.py`, `src/deploy/export_norm_header.py`, `src/deploy/tflm_check_ops.py`
- `src/tinyol/tinyol_sim.py`
- `src/run_all.py`, `src/smoke/run_smoke.py`
- `deploy/arduino_infer/arduino_infer.ino`, `deploy/arduino_tinyol/arduino_tinyol.ino`
- `tests/*.py`

## Remaining External Steps (manual/hardware-dependent)
- [ ] Install dependencies inside conda env `tinymlproj` and verify TensorFlow CUDA runtime.
- [ ] Install Arduino toolchain (`arduino-cli`) and board core.
- [ ] Compile/upload Arduino sketches and capture Flash/RAM/latency.
- [ ] Power measurement run (optional hardware path).

## Smoke Command
```bash
python -m src.smoke.run_smoke --config configs/smoke.yaml
```

## Full Pipeline Command
```bash
python -m src.run_all --config configs/default.yaml
```
