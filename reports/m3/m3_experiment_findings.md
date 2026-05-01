# M3 experiment findings

Interpretation of aggregated results from `m3_domain_comparison.csv` and `m3_experiment_master_all.csv`. Covers all seven model variants across experiments **E00–E12** (E01 and E02 not run in this batch). **E11** / **E12** are the T=50 counterparts of **E09** / **E10** (same protocols, 2.5 s @ 20 Hz); Slurm scripts `scripts/slurm/job_m3_seq_e11_t50_all_models.sh` and `job_m3_seq_e12_t50_all_models.sh`. Per-checkpoint WISDM test scores are in §9 and in `m3_cross_eval_wisdm.csv`.

---

## Experiment index

| Experiment | Description |
|------------|-------------|
| **E00** | WISDM M2 anchor — train and evaluate entirely on WISDM (source-only baseline) |
| **E01** | *(not run)* WISDM user holdout split |
| **E02** | *(not run)* Arduino zero-shot at 100 Hz, T=500 window |
| **E03** | Arduino zero-shot — raw units, no conversion, T=100, 20 Hz |
| **E04** | Arduino zero-shot — unit fix: WISDM→g, Arduino firmware ÷4 undone (`wisdm_to_g`) |
| **E05** | Arduino zero-shot — legacy unit fix: Arduino converted to m/s² (`arduino_to_mps2_legacy`) |
| **E06** | Arduino zero-shot — no normalization at training or inference (ablation) |
| **E07** | Arduino zero-shot — train with z-score but **skip** normalization at inference (ablation) |
| **E08** | Arduino zero-shot — raw units, T=50 window (window-size ablation) |
| **E09** | Pretrain on WISDM, **fine-tune** on Arduino train split, evaluate Arduino test split (**T=100**) |
| **E10** | Train **from scratch** on Arduino train split, evaluate Arduino test split (**T=100**) |
| **E11** | Same protocol as **E09**, **T=50** (2.5 s @ 20 Hz) — apples-to-apples window comparison vs E09 |
| **E12** | Same protocol as **E10**, **T=50** — apples-to-apples window comparison vs E10 |

---

## 1. Without any adaptation, domain gap is total (E03)

All seven models collapse to approximately **0.167 accuracy** on Arduino — chance level for 6 classes. A model that reached ~99% on WISDM is effectively guessing on Arduino raw data. This confirms a severe domain gap even at the raw-unit level.

---

## 2. Unit conversion alone recovers roughly half (E04 vs E05)

Fixing physical units (WISDM raw counts → g; Arduino firmware ÷4 undone) recovers **0.48–0.58** accuracy on Arduino — a 3× jump from chance. The two conversion strategies (**E04** `wisdm_to_g` and **E05** `arduino_to_mps2_legacy`) perform almost identically across all models, indicating the dominant factor is sensor scaling, not specific conversion formula.

| Model | E03 (raw, no fix) | E04 (wisdm_to_g) | E05 (legacy_mps2) |
|-------|-------------------|------------------|-------------------|
| daghero | 0.166 | 0.508 | 0.509 |
| deepconv_lstm | 0.176 | 0.583 | 0.571 |
| repmobile | 0.167 | 0.487 | 0.484 |
| tcn_attention | 0.167 | 0.512 | 0.594 |
| tcn_inception | 0.166 | 0.502 | 0.540 |
| xtinyhar | 0.167 | 0.522 | 0.525 |
| xtinyhar_relu | 0.167 | 0.571 | 0.564 |

`tcn_attention` is the outlier — it benefits more from the legacy m/s² conversion (0.594 vs 0.512), suggesting its attention mechanism leverages absolute scale differences.

---

## 3. Normalization is non-negotiable (E06, E07)

- **E06** — train with no normalization, infer with no normalization → chance level (~0.167) for almost all models.
- **E07** — train with z-score, but **skip** normalization at inference → same collapse everywhere.
- `tcn_attention` in E06 holds at ~0.35 FP32 (attention partially compensates). Even it fails in E07, showing that what matters is **consistency** between training and inference.

**Key takeaway:** z-score normalization must match between training and inference. Omitting it at either stage is fatal.

---

## 4. Shorter window (T=50) does not help zero-shot — but reduces latency significantly (E08)

Under zero-shot transfer with raw units, T=50 still yields chance-level accuracy (~0.167). The window length does not address the root cause (unit/scale mismatch).

However, in terms of **model size and inference latency**, T=50 does have real effects:

| Model | Size T=100 (KB) | Size T=50 (KB) | Latency T=100 (ms) | Latency T=50 (ms) | Latency ratio |
|-------|-----------------|----------------|--------------------|--------------------|---------------|
| daghero | 26.1 | 26.1 | 0.078 | 0.045 | 1.73× |
| deepconv_lstm | **136.9** | **107.6** | 4.26 | 2.05 | **2.08×** |
| repmobile | 42.1 | 42.1 | 0.332 | 0.177 | 1.87× |
| tcn_attention | 578.4 | 578.4 | 8.30 | 4.42 | 1.88× |
| tcn_inception | 369.9 | 369.9 | 2.40 | 1.31 | 1.83× |
| xtinyhar | 315.2 | 311.5 | 0.327 | 0.326 | 1.00× |
| xtinyhar_relu | 312.4 | 308.6 | 0.337 | 0.325 | 1.04× |

- **`deepconv_lstm`** shrinks by ~29 KB and inference halves — the LSTM is the only architecture where the temporal dimension directly drives model size.
- **TCN and RepMobile** see no size change (convolutional weights don't depend on input length), but latency nearly halves because fewer time steps are processed.
- **XtinyHAR** variants see almost no latency gain — the bottleneck is not temporal computation.
- **E11** and **E12** use the same protocols as **E09** / **E10** at **T=50**; Arduino FP32 and latency numbers are summarized in **§6a** (and full rows in `m3_experiment_master_all.csv`).

---

## 5. Fine-tuning closes the gap almost completely (E09)

Pre-training on WISDM then fine-tuning on Arduino achieves **0.97–0.996** accuracy on Arduino — essentially matching the WISDM baseline for every model.

| Model | WISDM (E00) | Arduino fine-tune (E09) | Gap |
|-------|-------------|-------------------------|-----|
| daghero | 0.992 | **0.996** | +0.004 |
| deepconv_lstm | 0.988 | 0.994 | +0.006 |
| repmobile | 0.942 | 0.979 | +0.037 |
| tcn_attention | 0.994 | 0.995 | +0.001 |
| tcn_inception | 0.997 | 0.994 | −0.003 |
| xtinyhar | 0.957 | 0.979 | +0.022 |
| xtinyhar_relu | 0.936 | 0.973 | +0.037 |

Domain gap is effectively eliminated with fine-tuning. The weakest models (repmobile, xtinyhar variants) actually improve over their WISDM scores, likely because Arduino has a cleaner and more consistent recording setup.

---

## 6. Fine-tune vs from-scratch are nearly identical (E09 vs E10)

| Model | Fine-tune (E09) | From scratch (E10) | Δ |
|-------|-----------------|--------------------|---|
| daghero | 0.996 | 0.992 | +0.004 |
| deepconv_lstm | 0.994 | 0.987 | +0.007 |
| repmobile | 0.979 | 0.963 | +0.016 |
| tcn_attention | 0.995 | 0.993 | +0.002 |
| tcn_inception | 0.994 | 0.992 | +0.002 |
| xtinyhar | 0.979 | 0.979 | 0.000 |
| xtinyhar_relu | 0.973 | 0.973 | 0.000 |

WISDM pre-training adds at most ~0.016 accuracy points. Arduino is large enough to train most architectures from scratch without meaningful penalty. Pre-training is a safe default but not critical.

---

## 6a. T=50 vs T=100 after adaptation (E11 vs E09, E12 vs E10)

Same training recipe as §5–§6, but **window length 50 samples (2.5 s @ 20 Hz)** instead of 100. Numbers are **Arduino test FP32 accuracy** from `m3_experiment_master_all.csv` (`arch_seq` bundles; **E11/E12** include `deepconv_lstm` in the same matrix).

### Fine-tune (E09 T=100 vs E11 T=50)

| Model | E09 Arduino FP32 | E11 Arduino FP32 | Δ |
|-------|------------------|------------------|---|
| daghero | 0.996 | 0.987 | −0.008 |
| deepconv_lstm | 0.994 | 0.981 | −0.013 |
| repmobile | 0.979 | 0.968 | −0.012 |
| tcn_attention | 0.995 | 0.982 | −0.013 |
| tcn_inception | 0.994 | 0.981 | −0.013 |
| xtinyhar | 0.979 | 0.962 | −0.018 |
| xtinyhar_relu | 0.973 | 0.956 | −0.017 |

**Takeaway:** dropping to T=50 costs roughly **0.01–0.02** Arduino accuracy under fine-tuning, while **latency roughly halves** for depthwise / TCN stacks (see §4 pattern — e.g. `tcn_attention` mean latency **8.29 ms → 4.33 ms**, `deepconv_lstm` **4.25 ms → 2.05 ms** on the same hardware path in the master CSV).

### From-scratch (E10 T=100 vs E12 T=50)

| Model | E10 Arduino FP32 | E12 Arduino FP32 | Δ |
|-------|------------------|------------------|---|
| daghero | 0.992 | 0.989 | −0.004 |
| deepconv_lstm | 0.987 | 0.981 | −0.005 |
| repmobile | 0.963 | 0.951 | −0.012 |
| tcn_attention | 0.993 | 0.979 | −0.015 |
| tcn_inception | 0.992 | 0.987 | −0.006 |
| xtinyhar | 0.979 | 0.959 | −0.020 |
| xtinyhar_relu | 0.973 | 0.956 | −0.018 |

**Takeaway:** from-scratch shows the same qualitative trade: **small Arduino accuracy hit**, **substantial latency reduction** at T=50 for temporal-heavy models. WISDM-side behavior of these same checkpoints is in **§9.6–9.7**.

---

## 7. PTQ vs QAT across all models and key experiments

PTQ = post-training quantization (int8 calibration). QAT = quantization-aware training (fake-quant during fine-tuning or training).

### E00 — WISDM source-only baseline

| Model | FP32 | PTQ | QAT | PTQ drop | QAT drop | Status |
|-------|------|-----|-----|----------|----------|--------|
| daghero | 0.9921 | 0.9921 | 0.9930 | 0.0000 | −0.0009 | ok/ok |
| deepconv_lstm | 0.9884 | 0.9801 | 0.8238 | 0.0083 | **+0.1646** | ok/ok |
| repmobile | 0.9416 | 0.9418 | 0.9536 | −0.0001 | −0.0120 | ok/ok |
| tcn_attention | 0.9943 | 0.9939 | 0.9950 | 0.0004 | −0.0007 | ok/ok |
| tcn_inception | 0.9965 | 0.9965 | 0.9977 | 0.0000 | −0.0012 | ok/ok |
| xtinyhar | 0.9570 | 0.9562 | 0.9615 | 0.0007 | −0.0045 | **fail/fail** |
| xtinyhar_relu | 0.9365 | 0.9362 | 0.9511 | 0.0003 | −0.0146 | ok/ok |

### E09 — Fine-tune on Arduino

| Model | FP32 | PTQ | QAT | PTQ drop | QAT drop | Status |
|-------|------|-----|-----|----------|----------|--------|
| daghero | 0.9956 | 0.9956 | 0.9956 | 0.0000 | 0.0000 | ok/ok |
| deepconv_lstm | 0.9937 | 0.9842 | 0.8066 | 0.0095 | **+0.1871** | ok/ok |
| repmobile | 0.9791 | 0.9798 | 0.9703 | −0.0006 | 0.0088 | ok/ok |
| tcn_attention | 0.9949 | 0.9949 | 0.9956 | 0.0000 | −0.0006 | ok/ok |
| tcn_inception | 0.9937 | 0.9937 | 0.9949 | 0.0000 | −0.0013 | ok/ok |
| xtinyhar | 0.9791 | 0.9779 | 0.9823 | 0.0013 | −0.0032 | **fail/fail** |
| xtinyhar_relu | 0.9728 | 0.9735 | 0.9747 | −0.0006 | −0.0019 | ok/ok |

### E10 — Train from scratch on Arduino

| Model | FP32 | PTQ | QAT | PTQ drop | QAT drop | Status |
|-------|------|-----|-----|----------|----------|--------|
| daghero | 0.9924 | 0.9924 | 0.9962 | 0.0000 | −0.0038 | ok/ok |
| deepconv_lstm | 0.9867 | 0.9425 | 0.3382 | 0.0442 | **+0.6485** | ok/ok |
| repmobile | 0.9627 | 0.9627 | 0.9583 | 0.0000 | 0.0044 | ok/ok |
| tcn_attention | 0.9930 | 0.9924 | 0.9937 | 0.0006 | −0.0006 | ok/ok |
| tcn_inception | 0.9924 | 0.9924 | 0.9956 | 0.0000 | −0.0032 | ok/ok |
| xtinyhar | 0.9785 | 0.9779 | 0.9791 | 0.0006 | −0.0006 | **fail/fail** |
| xtinyhar_relu | 0.9735 | 0.9735 | 0.9804 | 0.0000 | −0.0070 | ok/ok |

**Observations:**
- **PTQ is stable** for every model except `deepconv_lstm` from scratch (E10: 0.044 drop). PTQ is generally safe to deploy.
- **QAT is excellent or better than FP32** for all models except `deepconv_lstm` — QAT improves most architectures by a small margin due to the regularization effect of fake-quant during training.
- **`deepconv_lstm` QAT collapse is systematic and worsens with dataset:** WISDM (−0.165), fine-tune (−0.187), from-scratch (**−0.649**). When trained natively on Arduino data the LSTM quantization breaks completely. This is a structural incompatibility with int8 QAT, likely due to LSTM gate activation ranges. PTQ is still usable for this model.
- **`xtinyhar_student_conv2d` (non-ReLU) fails PTQ and QAT everywhere** — across all experiments. The ReLU variant succeeds. Use `xtinyhar_student_conv2d_relu` for any quantized deployment.

---

## 8. Model size, latency, and Pareto analysis (T=100)

All sizes and latencies from E00 (WISDM baseline, representative of architecture):

| Model | Size (KB) | Latency mean (ms) | Latency p95 (ms) | E00 FP32 acc | E09 FP32 acc | Deploy viable? |
|-------|-----------|-------------------|------------------|--------------|--------------|----------------|
| **daghero** | **26.1** | **0.078** | 0.091 | 0.992 | 0.996 | Yes |
| repmobile | 42.1 | 0.332 | 0.355 | 0.942 | 0.979 | Yes |
| deepconv_lstm | 136.9 | 4.264 | 4.334 | 0.988 | 0.994 | PTQ only |
| xtinyhar | 315.2 | 0.327 | 0.342 | 0.957 | 0.979 | No (quant fails) |
| xtinyhar_relu | 312.4 | 0.337 | 0.348 | 0.936 | 0.973 | Yes |
| tcn_inception | 369.9 | 2.400 | 2.425 | 0.997 | 0.994 | Yes |
| tcn_attention | 578.4 | 8.300 | 8.572 | 0.994 | 0.995 | Yes |

**`daghero`** is the clear Pareto winner: ~22× smaller than `tcn_attention`, inference is ~106× faster, and accuracy is within 0.002. For any MCU with tight memory or real-time constraints, `daghero` is the recommended deployment model.

---

## 9. WISDM test accuracy of the same checkpoints (E03–E12)

Each row is the **saved FP32 checkpoint** for that experiment and architecture, evaluated on the **WISDM** held-out test (6834 windows at T=100 except E08/E11/E12 at T=50, 13923 windows). This makes the domain gap two-sided: you can read Arduino scores from the main aggregates and WISDM scores here. **`deepconv_lstm`** is not in these numbers for E03–E10 because those checkpoints live under `full_eXX/`, not the `arch_seq/` matrix — **it is included for E11/E12** since those were run through the new consolidated Slurm script which writes into `arch_seq/`.

### 9.1 Zero-shot trains (E03–E07): WISDM stays near-baseline while Arduino is broken

Models are trained only on WISDM then (for reporting elsewhere) evaluated on Arduino. On **their own** WISDM test split they remain strong. Representative **E03** (raw units) WISDM accuracy:

| Model | WISDM test acc (E03) |
|-------|---------------------|
| daghero | 0.994 |
| repmobile | 0.941 |
| tcn_attention | 0.994 |
| tcn_inception | 0.996 |
| xtinyhar | 0.954 |
| xtinyhar_relu | 0.949 |

**E04** and **E05** (unit fixes) and **E06** / **E07** (normalization ablations) stay within about **±0.01** of the E03 WISDM numbers per model — the protocol tweaks target cross-domain behavior on Arduino, not source-domain collapse.

### 9.2 E06 and E07: high WISDM, catastrophic Arduino — confirms *where* the failure is

E06 (no norm) and E07 (skip inference norm) still score **0.94–0.996** on WISDM for most architectures (e.g. daghero **0.994** on both; `tcn_attention` dips slightly on E06 at **0.989** vs **0.995** on E07). That matches §3: weights are not “untrained”; the failure mode is **inconsistent normalization / scale at Arduino inference**, not loss of WISDM discrimination in general.

### 9.3 E08 (T=50): WISDM accuracy stays high with the shorter window

| Model | WISDM test acc (E08, T=50) |
|-------|---------------------------|
| daghero | 0.985 |
| repmobile | 0.952 |
| tcn_attention | 0.990 |
| tcn_inception | 0.988 |
| xtinyhar | 0.953 |
| xtinyhar_relu | 0.955 |

So the T=50 window change does not wipe source-domain performance; it mainly changes window count and latency (§4).

### 9.4 E09 (pretrain WISDM → fine-tune Arduino): large WISDM forgetting

After fine-tuning on Arduino, the **same** final checkpoint on the **original** WISDM test split:

| Model | WISDM test acc (E09) |
|-------|---------------------|
| daghero | 0.570 |
| repmobile | 0.400 |
| tcn_attention | 0.670 |
| tcn_inception | 0.739 |
| xtinyhar | 0.435 |
| xtinyhar_relu | 0.441 |

**Takeaway:** Arduino performance recovers (§5), but **source-domain retention is poor** — the larger conv stacks retain more WISDM signal than the compact student models.

### 9.5 E10 (Arduino from scratch): ~chance-level on WISDM

Checkpoints never trained on WISDM labels; evaluated on the **E00** WISDM test tensors so the test set is comparable to other rows:

| Model | WISDM test acc (E10) |
|-------|---------------------|
| daghero | 0.394 |
| repmobile | 0.380 |
| tcn_attention | 0.359 |
| tcn_inception | 0.247 |
| xtinyhar | 0.265 |
| xtinyhar_relu | 0.271 |

Random guessing over six classes is **0.167**. These models sit **well above chance but far below a WISDM-trained model**, i.e. they pick up *some* correlated structure from accelerometer windows but **do not learn a WISDM-aligned classifier**.

### 9.6 E11 (pretrain WISDM → fine-tune Arduino, T=50): more forgetting than E09

E11 is identical to E09 but with a **T=50** window. WISDM forgetting is **worse** than E09 across the board, showing the shorter window makes it harder to retain the longer-range temporal patterns learned on WISDM:

| Model | WISDM test acc (E09, T=100) | WISDM test acc (E11, T=50) | Δ |
|-------|-------|-------|-------|
| daghero | 0.570 | 0.531 | −0.039 |
| deepconv_lstm | — | 0.622 | — |
| repmobile | 0.400 | 0.343 | −0.057 |
| tcn_attention | 0.670 | 0.572 | −0.098 |
| tcn_inception | 0.739 | 0.705 | −0.034 |
| xtinyhar | 0.435 | 0.564 | +0.129 |
| xtinyhar_relu | 0.441 | 0.548 | +0.107 |

`xtinyhar` variants are the exception — they actually retain slightly *more* WISDM signal at T=50. This likely reflects that the xtinyhar student's attention to local patterns is easier to preserve with shorter windows.

### 9.7 E12 (Arduino from-scratch, T=50): still near-chance on WISDM

| Model | WISDM test acc (E10, T=100) | WISDM test acc (E12, T=50) |
|-------|-------|-------|
| daghero | 0.394 | 0.365 |
| repmobile | 0.380 | 0.432 |
| tcn_attention | 0.359 | 0.350 |
| tcn_inception | 0.247 | 0.382 |
| xtinyhar | 0.265 | 0.349 |
| xtinyhar_relu | 0.271 | 0.321 |

All models remain well below any usable threshold — consistent with E10. The shorter T=50 window does not help or hurt meaningfully for from-scratch Arduino models on WISDM.

---

## 10. Summary of key findings

1. **Domain gap at raw units is 100% catastrophic** — all models drop to chance.
2. **Unit conversion alone is worth ~+33 accuracy points** (0.17 → 0.50) for free.
3. **Normalization consistency (train + inference) is mandatory** — skipping either one is fatal.
4. **Fine-tuning on Arduino data eliminates the domain gap** (0.97–0.996).
5. **Fine-tuning vs from-scratch gives at most ~0.016 difference** — pre-training is optional.
6. **PTQ is safe across all working architectures** — never more than 0.044 drop.
7. **QAT improves most models** but **destroys `deepconv_lstm`** (−0.187 to −0.649 depending on training data).
8. **`deepconv_lstm` should be PTQ-only** for Arduino-native training.
9. **`xtinyhar_student_conv2d` (non-ReLU) cannot be quantized** — always use the `_relu` variant.
10. **`daghero` dominates on size and speed** (26 KB, 0.08 ms) with near-top accuracy — best choice for MCU deployment.
11. **T=50 vs T=100 after adaptation (§6a):** on Arduino, fine-tune **(E11)** and from-scratch **(E12)** lose about **0.004–0.020** FP32 accuracy vs **E09** / **E10**, while latency tracks the same ~2× pattern as zero-shot **(§4)**. WISDM-side retention for those checkpoints is in **§9.6–9.7**.
12. **WISDM-side checkpoint scores (§9)** — zero-shot models (E03–E08) stay **~0.94–0.996** on WISDM while failing on Arduino; fine-tune **(E09/E11)** drops to **~0.34–0.74** on WISDM; from-scratch **(E10/E12)** is **~0.25–0.43** on WISDM (above chance **0.167** but not usable).

---

*Generated from M3 aggregate tables. Re-run aggregation after new experiments:*

```bash
cd /path/to/har-mcu
python -m src.m3.aggregate_masters --reports-dir reports/m3
```
