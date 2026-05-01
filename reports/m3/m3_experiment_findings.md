# M3 experiment findings

Interpretation of aggregated results (`m3_domain_comparison.csv`, `m3_experiment_master_all.csv`). Data are from the full M3 matrix (E00, E03–E10) across seven model variants.

---

## 1. Without any adaptation, domain gap is total (E03)

All seven models crash to approximately **0.167 accuracy** on Arduino — exactly 1/6 chance level (there are six classes). A model that reached ~99% on WISDM is effectively guessing on Arduino. This is a clear confirmation of the domain-gap problem.

---

## 2. Unit conversion alone recovers roughly half (E04, E05)

Fixing physical units (WISDM raw counts → g, Arduino firmware divide-by-four undone) recovers **about 0.50–0.58** on Arduino, a large jump from chance. E04 (`wisdm_to_g`) and E05 (legacy `arduino_to_mps2`) give almost identical results — both conversions are roughly equivalent. A large fraction of the gap is therefore **sensor scaling / units**, not only abstract “domain shift.”

---

## 3. Normalization is non-negotiable (E06, E07)

- **E06** — train and infer with no normalization at all → back to ~0.167, chance level for almost every model.
- **E07** — train with z-score but skip normalizing at inference → same collapse.
- The main exception is `tcn_attention_har_teacher` in E06, which holds at ~0.35 (attention may provide some scale robustness). Even that model collapses in E07.

**Takeaway:** z-score normalization must be applied consistently at training and inference. Omitting it at inference is as fatal as having no normalization.

---

## 4. Shorter windows do not fix zero-shot (E08)

Halving the window from T=100 to T=50 under zero-shot transfer still yields chance-level performance. The dominant issue for zero-shot here is not temporal resolution.

---

## 5. Fine-tuning closes the gap almost completely (E09)

Pre-training on WISDM then fine-tuning on Arduino reaches **about 0.97–0.996** on Arduino across models — comparable to strong WISDM-side performance. The domain gap largely disappears once there is target-domain supervision.

---

## 6. Fine-tune vs from-scratch are nearly identical (E09 vs E10)

| Model | Finetune (E09) | From scratch (E10) |
|-------|----------------|---------------------|
| daghero | 0.996 | 0.992 |
| deepconv_lstm | 0.994 | 0.987 |
| tcn_inception | 0.994 | 0.992 |
| repmobile | 0.979 | 0.963 |

Fine-tuning wins by roughly **0.003–0.016**. WISDM pre-training gives a modest benefit at best; the Arduino split appears large enough that from-scratch training reaches similar accuracy. Pre-training may still help with convergence or data efficiency, but final accuracy is close.

---

## 7. Largest model is not the best on accuracy alone (size vs accuracy)

| Model | Size | Inference (mean) | E00 WISDM FP32 acc |
|-------|------|------------------|---------------------|
| `daghero_cnn_2layer_conv2d` | **~26 KB** | **~0.08 ms** | ~0.992 |
| `repmobile_folded_conv2d` | ~42 KB | ~0.33 ms | ~0.942 |
| `deepconv_lstm_conv2d` | ~137 KB | ~4.3 ms | ~0.988 |
| `tcn_inception_conv2d` | ~370 KB | ~2.4 ms | **~0.996** |
| `tcn_attention_har_teacher_conv2d` | **~578 KB** | **~8.3 ms** | ~0.994 |

`daghero` is vastly smaller and faster than `tcn_attention` while staying within a few points of the best WISDM accuracy. For MCU deployment it is the clearest **Pareto** choice on size, latency, and accuracy.

---

## 8. DeepConv-LSTM shows severe QAT collapse on E10

When trained from scratch on Arduino, `deepconv_lstm` reaches high FP32 accuracy (~0.987) but QAT accuracy drops to **~0.338** — a large collapse. Under fine-tuning (E09) the QAT drop is smaller but still notable relative to other architectures. Other models in the matrix show stable QAT (small drops or comparable accuracy).

**Implication:** treat this architecture with extra care for int8 QAT on Arduino-native data; consider architecture or training changes before relying on quantized deployment.

---

## 9. `xtinyhar_student_conv2d` (non-ReLU) fails PTQ/QAT everywhere

Across experiments, the non-ReLU XtinyHAR variant reports **PTQ/QAT failed** while `xtinyhar_student_conv2d_relu` succeeds. Likely causes include activation ranges that are harder to quantize; the ReLU variant is the practical choice for quantized pipelines.

---

## One-sentence summary

**Unit conversion plus consistent z-score normalization recovers a large fraction of zero-shot performance for free; fine-tuning on Arduino data removes most of the remaining gap; for MCU deployment `daghero` dominates on size, speed, and accuracy; DeepConv-LSTM needs extra scrutiny for QAT on Arduino data; use the ReLU XtinyHAR variant for quantization.**

---

*Generated from the M3 aggregate tables. Re-run aggregation after new jobs:*

```bash
cd /path/to/har-mcu
python -m src.m3.aggregate_masters --reports-dir reports/m3
```
