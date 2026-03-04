# Real-Time Human Activity Recognition on Microcontrollers: A Quantization-Aware Deep Learning Approach

_Hamza A. Abushahla, Ariel Justine N. Panopio, Layth Al-Khairulla, and Dr. Mohamed Hassan_

This repository contains the full implementation and supplementary materials for our research project, **"Real-Time Human Activity Recognition on Microcontrollers: A Quantization-Aware Deep Learning Approach,"** completed as part of the COE 59413 Tiny Machine Learning course at the American University of Sharjah.

## Dataset 

This work uses the **Wireless Sensor Data Mining (WISDM)**[^1][^2] dataset as our primary public benchmark for human activity recognition (HAR). The dataset consists of **1,098,207 labeled samples** of motion data collected from **36 users** performing **six activities** over specific time periods: walking, jogging, sitting, standing, and ascending and descending stairs. The signals were recorded using smartphone accelerometers, which measure linear acceleration along three axes and can indirectly capture device orientation. Data were sampled at **20 Hz** (1 sample every 50 ms), yielding 20 samples per second.

Each record in the raw dataset contains:

- **User ID**: integer identifier of the subject (1–36).
- **Activity label**: one of `Walking`, `Jogging`, `Upstairs`, `Downstairs`, `Sitting`, or `Standing`.
- **Timestamp**: nanosecond-resolution time at which the sample was recorded.
- **X-axis acceleration**: acceleration along the x dimension (in device coordinates).
- **Y-axis acceleration**: acceleration along the y dimension.
- **Z-axis acceleration**: acceleration along the z dimension.


> **Class distribution:** The WISDM dataset is *class-imbalanced*—some activities have many more samples than others. The table below reports the number of samples per activity in the raw dataset:

| Activity     | Count    |
|--------------|----------|
| Walking      | 424,400  |
| Jogging      | 342,177  |
| Upstairs     | 122,869  |
| Downstairs   | 100,427  |
| Sitting      | 59,939   |
| Standing     | 48,395   |

<img src="figures/class_distribution.png"
     alt="WISDM class distribution (number of samples per activity)"
     width="500">

*Figure 1. Class distribution in the WISDM dataset (number of samples per activity).* 



[^1]: https://dl.acm.org/doi/abs/10.1145/1964897.1964918
[^2]: https://www.cis.fordham.edu/wisdm/dataset.php 

## Reproducible Pipeline (TensorFlow 2.14.1 CUDA + TFLite Micro)

### Environment

Use conda environment `tinymlproj`.

Optional: update conda first:

```bash
conda update -n base -c defaults conda -y
```

#### Option A (Recommended): install with `environment.yml`

```bash
conda env create -f environment.yml
conda activate tinymlproj
```

If `tinymlproj` already exists:

```bash
conda activate tinymlproj
conda env update -n tinymlproj -f environment.yml --prune
```

#### Option B: install with `requirements.txt` in an existing env

```bash
conda create -n tinymlproj "python<3.11" -y
conda activate tinymlproj
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### Option C: manual package install (your current flow)

```bash
conda create -n tinymlproj "python<3.11" -y
conda activate tinymlproj
python -m pip install --upgrade pip
python -m pip install "numpy<2" pandas scikit-learn scipy matplotlib seaborn "tensorflow[and-cuda]==2.14.1" tensorflow-model-optimization==0.8.0 nvidia-cuda-nvrtc-cu11==11.8.89 PyYAML tqdm ipykernel jupyterlab notebook pytest
```

Validate TensorFlow/CUDA runtime after activation:

```bash
python scripts/env/check_tf_cuda.py --expect-version 2.14.1 --require-gpu
python scripts/env/check_versions.py
```

Register the notebook kernel once:

```bash
python -m ipykernel install --user --name tinymlproj --display-name "Python (tinymlproj)"
```

If you see TensorFlow/XLA logs like `Start cannot spawn child process: No such file or directory`, update the env and restart Jupyter kernel:

```bash
conda activate tinymlproj
conda env update -n tinymlproj -f environment.yml --prune
```

If you see `Could not load library libcudnn_cnn_infer.so.8 ... libnvrtc.so: cannot open shared object file`, make sure `nvidia-cuda-nvrtc-cu11` is installed, then restart the kernel and rerun notebook cell 1:

```bash
conda activate tinymlproj
conda env update -n tinymlproj -f environment.yml --prune
```

If you see TensorFlow logs about NUMA (for example `could not open file to read NUMA node` or `Could not identify NUMA node of platform GPU id 0`), those are informational on many desktop kernels and are not the failure cause by themselves.

If notebook training fails with `TypeError: Object of type float32 is not JSON serializable`, the failure is from writing Keras history/report JSON. This repo now uses shared JSON-safe serialization in pipeline scripts. Pull latest changes, restart the kernel, and rerun `notebooks/replication_deepconvlstm.ipynb` from cell 7 onward.

If paper notebooks fail during FP32 evaluation with `TypeError: 'str' object is not callable`, the typical cause is stale kernel state or custom-layer deserialization mismatch after code updates. Restart the kernel, rerun the notebook from the first cell, and retrain so fresh checkpoints are created with the current serialization code.
The 5 paper notebooks now enable project-module auto-reload in the first cell and fail fast if the safe loader path is not active.

### Fast smoke test

```bash
python -m src.smoke.run_smoke --config configs/smoke.yaml
```

### Full pipeline

```bash
python -m src.run_all --config configs/default.yaml
```

`run_all` now reports an overall status and exits non-zero if any protocol fails strict PTQ or QAT deployability gates.

### DeepConvLSTM replication notebook

Launch Jupyter:

```bash
jupyter lab
```

Open `notebooks/replication_deepconvlstm.ipynb` and run in this order:
1. Preflight/runtime cells
2. Quick mode (`RUN_MODE="quick"`) for sanity
3. Full mode (`RUN_MODE="full"`) for replication results

#### Paper Strict Mode (Nano 33 BLE Sense)

The replication notebook and quantization pipeline use two complementary tracks:
- Replication-metric track: host-side TFLite accuracy/size reporting for PTQ and QAT.
- Strict deployment track: full-integer I/O plus TFLM op compatibility for Nano deployability.

Strict policy defaults:
- Full-integer strict mode enabled for both PTQ and QAT (`strict_full_int8=true`).
- TFLM op compatibility required (`require_tflm_compatible=true`).
- Accepted integer I/O dtypes: `int8` and `uint8`.
- Mixed-precision/`SELECT_TF_OPS` fallback is not used for deployment acceptance.

Why `status=error` can appear with valid quantized I/O:
- Conversion can succeed and still produce control-flow ops (for example `WHILE`, `FILL`, `EXPAND_DIMS`) that are outside the configured TFLM resolver set.
- In that case, replication metrics may still be available on host TFLite, but strict deployability is marked failed.

Notebook toggles:
- `RUN_QAT=True` by default.
- `STRICT_FULL_INT8=True`
- `REQUIRE_TFLM_COMPAT=True`
- `FAIL_ON_PTQ_ERROR=False` to keep notebook flow alive and report PTQ failure rows.
- `FAIL_ON_QAT_ERROR=False` to keep notebook flow alive and report QAT failure rows.
- Two calibration variants are reported:
  - `traincal`: representative data from train split.
  - `authorcal`: representative data from test split (`AUTHOR_STYLE_REP_SAMPLES=100`) to mirror the reference notebook style.

Key artifacts are generated in:
- `data/processed/`
- `checkpoints/`
- `models_tflite/`
- `reports/`
- `deploy/common/`

### Paper Replication notebooks (WISDM-first, PTQ/QAT-only)

Use these notebooks for the 5-paper reproducibility track:

- `notebooks/replication_xtinyhar.ipynb`: XTinyHAR student adaptation on WISDM.
- `notebooks/replication_repmobile.ipynb`: RepMobile folded architecture adaptation.
- `notebooks/replication_tcn_attention_har.ipynb`: TCN-attention-HAR teacher adaptation.
- `notebooks/replication_daghero_qadnn.ipynb`: Daghero quantized/adaptive CNN adaptation.
- `notebooks/replication_tcn_inception.ipynb`: TCN-Inception adaptation.

#### Conv1D -> Conv2D QAT-safe policy for paper notebooks

To keep PTQ/QAT reproducible with `tensorflow==2.14.1` and `tensorflow-model-optimization==0.8.0`, the default paper configs use Conv2D-equivalent variants:

- XTinyHAR: `xtinyhar_student` -> `xtinyhar_student_conv2d`
- RepMobile: `repmobile_folded` -> `repmobile_folded_conv2d`
- TCN-attention-HAR: `tcn_attention_har_teacher` -> `tcn_attention_har_teacher_conv2d`
- Daghero CNN: `daghero_cnn_2layer` -> `daghero_cnn_2layer_conv2d`
- TCN-Inception: `tcn_inception` -> `tcn_inception_conv2d`

Mapping rule:
- `Conv1D(filters, k)` on `(B, T, C)` is mapped to `Conv2D(filters, (k, 1))` on `(B, T, 1, C)`.
- For RepMobile, SeparableConv1D is mapped explicitly to `DepthwiseConv2D((k,1)) + Conv2D((1,1))` (depthwise + pointwise decomposition).

Original Conv1D builders remain in the codebase for traceability and manual experimentation, but the default WISDM paper configs point to `*_conv2d` variants.

TFMOT transform semantics for SeparableConv layers:
- `SeparableConv1DQuantize`: rewrites a `SeparableConv1D` path into a quantization-compatible `SeparableConv2D` representation (with shape expansion/squeeze around time axis).
- `SeparableConvQuantize`: applies the default 8-bit separable-convolution transform on the 2D form (effectively quantization-aware decomposition into depthwise + pointwise operations).
This repository keeps the production replication path on Conv2D-safe RepMobile (`repmobile_folded_conv2d`) and does not enable native SeparableConv1D QAT execution in notebooks/config defaults.

Recommended run modes in each notebook:

- `RUN_MODE="sanity_check"`: quick validation runs; GPU-first execution for all stages (including QAT), with CPU fallback when configured.
- `RUN_MODE="full_run"`: full-length runs; GPU-first execution for all stages (including QAT), with CPU fallback when configured.

QAT runtime fallback behavior:
- `quant.qat.device_preference` controls whether QAT attempts `gpu` or `cpu` first.
- `quant.qat.auto_fallback_to_cpu=true` enables automatic retry on CPU when GPU QAT hits known deterministic fake-quant limitations or GPU is unavailable.
- QAT export JSON now records `qat_device_attempted`, `qat_device_used`, `fallback_triggered`, and `fallback_reason`.

Comparison and reporting in these 5 notebooks follow the same style as `replication_deepconvlstm.ipynb`, adapted to paper-specific framing:
- `paper target` rows (when available) + `WISDM replication` rows for FP32/PTQ/QAT.
- accuracy comparison bar chart, quantized size table, latency (median+p95) chart.
- reproducibility drift table from repeat FP32 checkpoint evaluation.
- markdown exports are generated without optional `tabulate` dependency.

Notebook report rendering is centralized in:
- `src/eval/notebook_reporting.py`
- `render_paper_notebook_report(cfg, out, drift_tol=1e-9)`

Each paper notebook now keeps the experiment run cell and delegates report rendering to this shared helper so UX changes propagate across all 5 notebooks.

DeepConv parity note for strict deploy checks:
- The 5 paper notebooks now print strict-gate config inputs up front (`strict_full_int8`, `require_tflm_compatible`, accepted integer I/O dtypes, plus legacy profile/override config fields for audit visibility).
- Each notebook shows a standardized **Strict Deploy-Gate Details** table per protocol and tier (PTQ/QAT), sourced from `ptq_report_json` and `qat_report_json`.
- `failed` in that table means strict MCU deployability failed under the configured gate, even when host TFLite metrics are strong.
- With fixed `run_id=wisdm_r0`, rerun notebooks top-to-bottom to overwrite older artifacts; notebooks warn if legacy report payload fields are detected.

TFLite interpreter policy for paper/utility evaluation:
- Shared `evaluate_tflite` now uses `tf.lite.experimental.OpResolverType.BUILTIN_WITHOUT_DEFAULT_DELEGATES` with `experimental_delegates=[]`.
- This prevents desktop XNNPACK delegate injection from showing `DELEGATE` pseudo-ops and keeps op inspection MCU-relevant.
- PTQ reporting in paper notebooks prints two op views per protocol:
  - `interpreter_ops`: delegate-free runtime op list from `_get_ops_details()`.
  - `tflm_ops`: flatbuffer op list from strict deploy-gate compatibility inspection.
- The CLI op checker (`python -m src.deploy.tflm_check_ops`) now uses the same delegate-free interpreter settings for consistency.
- Strict gate compatibility source-of-truth is now:
  - `micro_mutable_op_resolver.h` from TFLM main:
    https://github.com/tensorflow/tflite-micro/blob/main/tensorflow/lite/micro/micro_mutable_op_resolver.h
- `deploy.allowed_ops_profile` and `deploy.allowed_ops` remain in config as legacy/non-gating fields during transition.
- PTQ/QAT export reports persist `allowed_ops_profile` / `allowed_ops_used` for backward compatibility and audit trails.

TFLM support gate source of truth:
- Deploy-gate pass/fail is derived from micro-mutable op capability (`micro_mutable_op_resolver.h`) only.
- `failed` means unsupported by that TFLM-version capability list.
- Caveat: this is still not a universal per-MCU runtime guarantee; MCU memory/toolchain/firmware resolver constraints can still block deployment.
- PTQ/QAT export payloads include transparency fields:
  - `compatibility_scope`
  - `unsupported_ops_micro_mutable` (canonical unsupported list)
  - `unsupported_ops` (backward-compatible alias)
  - `possibly_supported_upstream_tflm`
  - `unsupported_in_reference`

Arduino resolver synchronization:
- Arduino sketches in `deploy/` now include additional resolver registrations aligned with surfaced model ops and micro-mutable capability (`AddBatchMatMul`, `AddBatchToSpaceND`, `AddSpaceToBatchNd`, `AddConcatenation`, `AddFill`, `AddPad`, `AddRsqrt`, `AddSquaredDifference`, `AddSub`).
- If your pinned Arduino TFLM package is older and missing one of these methods, set `HAR_TFLM_ENABLE_MICRO_MUTABLE_ONLY_EXTRA_OPS` to `0` in the sketch and rebuild.

If QAT fails with a message about `Conv1D`/`SeparableConv1D` not being supported, verify that the notebook is using the Conv2D-safe `model_variant` from `configs/papers/*.yaml` (`*_conv2d`).

### What `run_paper_experiment` does

`src/run_paper_experiment.py` executes the full paper pipeline for each split protocol:

1. Train FP32 model from the selected paper model variant.
2. Evaluate FP32 model and save metrics + confusion matrix.
3. Export PTQ INT8 model and run strict deploy-gate checks.
4. Evaluate PTQ TFLite model (accuracy/F1/confusion/latency).
5. Run QAT (if enabled), export INT8 model, and run strict deploy-gate checks.
6. Evaluate QAT TFLite model (accuracy/F1/confusion/latency).
7. Save per-run artifacts, per-paper summaries, master summaries, and per-paper comparison charts/tables.

Compression policy is explicitly enforced: `experiment.compression_focus` must be `ptq_qat_only`.
KD details from papers are documented for context only and are not executed in this pipeline.

### PTQ/QAT status fields (important)

Paper-run result rows include `ptq_status` and `qat_status`. These are **strict deploy-gate statuses**, not host-accuracy statuses.

- `ok`: quantized export passed strict deployability checks.
- `failed`: quantized export failed strict deployability checks (for example unsupported TFLM ops), even if host TFLite accuracy/F1 is high.
- `skipped`: QAT stage was not run (`quant.qat.enabled=false`) or was intentionally skipped.

In short: `ptq_status=failed` or `qat_status=failed` means **strict MCU deployability check failed** under the configured gate (`strict_full_int8` and/or `require_tflm_compatible`), not that notebook execution failed.

For Conv2D-safe paper models, Arduino resolver registration in this repo's `deploy/` sketches has been expanded to include commonly surfaced kernels (`MAX_POOL_2D`, `MEAN`, `DEPTHWISE_CONV_2D`, and additional ops used by attention-style models), but strict deploy-gate pass/fail remains micro-mutable-only.

### What is saved and where

Primary save locations:

- `checkpoints/`
  - FP32 checkpoints: `<model>_T<window>_P<protocol>_<run_id>.keras`
  - FP32 history JSON
  - QAT checkpoint + QAT history JSON
- `models_tflite/`
  - FP32 float `.tflite` (used for `fp32_model_size_kb` measurement)
  - PTQ INT8 `.tflite`
  - QAT INT8 `.tflite`
- `reports/<paper_slug>/`
  - `*_results_<protocol>.csv`
  - `<paper_slug>_summary.md`
  - stage metrics JSON/MD for FP32/PTQ/QAT
  - confusion matrices (FP32/PTQ/QAT)
  - training curves (FP32/QAT)
  - run artifacts (`artifacts/*.json`)
- `reports/<paper_slug>/comparison/`
  - `<paper_slug>_comparison.csv`
  - `<paper_slug>_comparison.md`
  - accuracy/model-size/latency PNG charts
- `reports/results_master.csv`
- `reports/results_master.md`

### Metrics schema (paper notebooks)

Each run records:

- FP32/PTQ/QAT: `accuracy`, `macro_f1`
- Classification report JSON and confusion matrix plot paths
- Model size:
  - `fp32_model_size_kb` (measured from exported float `.tflite`)
  - `ptq_model_size_kb`, `qat_model_size_kb`
- Training time:
  - `fp32_training_time_sec`
  - `qat_training_time_sec`
- TFLite inference timing (CPU host interpreter):
  - `inference_latency_ms_median`
  - `inference_latency_ms_p95`
  - `inference_latency_ms_mean`
  - `warmup_samples`, `timed_samples`
- TFLite op-inspection fields:
  - `interpreter_ops` (delegate-free runtime op names from evaluator)
  - `interpreter_op_count`
- Deploy-gate fields:
  - `status`, `full_integer_io`, `tflm_compatible`
  - `unsupported_ops_micro_mutable` (canonical)
  - `unsupported_ops` (backward-compatible alias)
  - `allowed_ops_profile`, `allowed_ops_used` (legacy/non-gating)
- Row-level quant stage statuses:
  - `ptq_status`, `qat_status` (`ok` / `failed` / `skipped`; strict deploy-gate meaning)

Converter logs/warnings:
- Messages such as `Statistics for quantized inputs were expected...`, `Ignored output_format`, and SavedModel loading traces are informational.
- Deploy-gate pass/fail is determined by integer I/O checks and micro-mutable compatibility checks, not by those warnings.

### Arduino deployment

1. Export model and normalization headers:

```bash
python -m src.deploy.export_c_array --tflite models_tflite/<model>.tflite --out-dir deploy/common
python -m src.deploy.export_norm_header --norm-json data/processed/<norm_stats>.json --out deploy/common/norm_stats.h
```

2. Use `deploy/arduino_infer/arduino_infer.ino` for inference profiling.
3. Use `deploy/arduino_tinyol/arduino_tinyol.ino` for TinyOL-style online head updates.
