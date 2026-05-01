# M3 experiment findings

Interpretation of aggregated results from `m3_domain_comparison.csv`, `m3_experiment_master_all.csv`, and (when present) **`m3_cross_eval_wisdm.csv`** — the last file lists eval-only WISDM test scores for checkpoints from E03–E10 (see §9). Covers all seven model variants across experiments E00–E10 (E01 and E02 not run in this batch). **E11/E12** (T=50 finetune / from-scratch) are optional Slurm follow-ups: `scripts/slurm/job_m3_seq_e11_t50_all_models.sh` (seven models in one job), `scripts/slurm/job_m3_seq_e12_t50_all_models.sh` (same).

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
- A proper accuracy comparison at T=50 for E09/E10 (fine-tuned or from-scratch) **was not run**, so the accuracy vs window tradeoff under realistic conditions is not yet established.

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

## 9. Post-hoc WISDM cross-eval (E03–E10, CPU-only)

Slurm configs typically set a single `eval_domain` per run, so the main aggregate tables do **not** by themselves list “same checkpoint on both WISDM and Arduino test.” After the fact, `python scripts/run_cross_eval_wisdm.py` loads each saved FP32 checkpoint and runs inference on the appropriate processed WISDM test arrays (E03–E08: `source_wisdm/`; E09: `pretrain_wisdm/` for forgetting; E10: E00 WISDM split). Re-run `python -m src.m3.aggregate_masters --reports-dir reports/m3` to refresh **`m3_cross_eval_wisdm.csv`** / `.md` from `reports/m3/cross_eval/*.json`.

**How this differs from `m3_domain_comparison.csv`:** the `wisdm_fp32_accuracy` column there is the **E00 source-only anchor** joined onto Arduino rows for the same `model_variant`. The cross-eval table is the **actual WISDM test accuracy** of the checkpoint trained under E03–E10 protocols — e.g. E09/E10 rows show catastrophic forgetting or no WISDM knowledge, while E06/E07 still look strong on WISDM because the collapse was on Arduino zero-shot only.

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
11. **T=50 window halves inference latency** for LSTM and TCN architectures but a proper accuracy comparison under fine-tuning/from-scratch was not run and should be a follow-up experiment.

---

*Generated from M3 aggregate tables (including `m3_cross_eval_wisdm` when JSONs exist). Re-run aggregation after new experiments:*

```bash
cd /path/to/har-mcu
python -m src.m3.aggregate_masters --reports-dir reports/m3
```
