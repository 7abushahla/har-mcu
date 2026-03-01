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

### Arduino deployment

1. Export model and normalization headers:

```bash
python -m src.deploy.export_c_array --tflite models_tflite/<model>.tflite --out-dir deploy/common
python -m src.deploy.export_norm_header --norm-json data/processed/<norm_stats>.json --out deploy/common/norm_stats.h
```

2. Use `deploy/arduino_infer/arduino_infer.ino` for inference profiling.
3. Use `deploy/arduino_tinyol/arduino_tinyol.ino` for TinyOL-style online head updates.

### TFLite Micro vendor pin

Commit pin metadata lives at `third_party/tflite-micro/VERSION_PIN.md`.
Vendor the full TFLM source tree in that directory at the pinned commit for reproducible embedded builds.
