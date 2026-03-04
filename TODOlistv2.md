# TODOlistv2.md — WISDM-First 5-Paper HAR Reproducibility Spec

## Scope and locked defaults
- Notebook set (5): `XTinyHAR`, `RepMobile`, `TCN-attention-HAR`, `Daghero (Quantized+Adaptive CNN)`, `TCN-Inception`.
- Execution priority: **WISDM-first** for all five models.
- Paper-faithful protocols are documented per paper; WISDM adaptation is the first implementation milestone.
- Existing DeepConvLSTM path remains operational and backward compatible.

## Implemented updates (2026-03-04)
- Shared TFLite evaluator now uses delegate-free interpreter construction:
  - `experimental_op_resolver_type = BUILTIN_WITHOUT_DEFAULT_DELEGATES`
  - `experimental_delegates = []`
  - `num_threads = 1`
- This change is implemented globally in `src/eval/eval_tflite.py` (not paper-only), so paper runs/smoke/other shared calls avoid XNNPACK `DELEGATE` pseudo-op artifacts.
- CLI op checker now uses the same delegate-free policy in `src/deploy/tflm_check_ops.py`.
- TFLite eval metrics now persist:
  - `interpreter_ops`
  - `interpreter_op_count`
- Strict deploy-gate allowlist is now config-driven:
  - `deploy.allowed_ops_profile`
  - `deploy.allowed_ops` (optional explicit override)
- PTQ/QAT export artifacts now persist:
  - `allowed_ops_profile`
  - `allowed_ops_used`
- All 5 paper notebooks now print a dedicated PTQ operator visibility block per protocol:
  - `interpreter_ops` (delegate-free runtime view)
  - `tflm_ops` (flatbuffer/deploy-gate view)
  - non-fatal mismatch warning with op-count deltas.
- Strict deploy-gate status semantics remain unchanged:
  - `ptq_status` / `qat_status` are strict MCU deployability statuses, not host-accuracy statuses.
- Arduino resolver alignment:
  - `deploy/arduino_infer/arduino_infer.ino` and `deploy/arduino_tinyol/arduino_tinyol.ino` now register Conv2D-model common ops (`DepthwiseConv2D`, `MaxPool2D`, `Mean`) to stay aligned with the extended gate profile.
- Converter warning policy:
  - quantization conversion warnings/log lines are documented as informational; pass/fail is controlled by strict gate checks (integer I/O + configured compatibility allowlist).

## GitHub Verification Log
| paper | official_repo | status | checked_date | notes |
|---|---|---|---|---|
| XTinyHAR | https://github.com/Ism-ail11/XTinyHAR | listed by paper and used as source-of-truth | 2026-03-03 | paper DOI: https://doi.org/10.1038/s41598-025-26297-2 |
| RepMobile | https://github.com/Yuki0614/RepMobile | listed by paper and used as source-of-truth | 2026-03-03 | paper DOI: https://doi.org/10.1109/JSEN.2024.3424578 |
| TCN-attention-HAR | none declared by paper | no official repo found in paper | 2026-03-03 | non-authoritative implementation noted: https://github.com/zhuwei55555/TCN-attention-HAR |
| Daghero Quantized+Adaptive | none single official training repo in paper | no single official repo found | 2026-03-03 | toolchain context repos: PLiNIO/DORY/PULP-NN |
| TCN-Inception | none declared by paper | no official repo found | 2026-03-03 | paper DOI: https://doi.org/10.1016/j.future.2024.05.023 |

## Known Contradictions
- TCN-attention-HAR reports `heads=8` in one parameter section, but its tuning discussion selects `heads=4` as final; both must be logged and tested.
- XTinyHAR paper final settings must override any quick/demo defaults from repo scripts.
- RepMobile repo defaults can differ from paper epoch scheduling by dataset; paper schedule is authoritative for replication specs.

## Do Not Assume
- Any missing split rule, preprocessing detail, or augmentation behavior must be written to `reports/paper_specs_<slug>.md` under `assumptions`.
- If official repo is missing or incomplete, mark it explicitly and provide implementation assumptions with rationale.
- Paper metrics and WISDM-adaptation metrics must never be mixed in a single target row.

---

## Paper 1 — XTinyHAR
### Paper Facts (verbatim-verified)
- Citation: Scientific Reports (2025), DOI https://doi.org/10.1038/s41598-025-26297-2
- Original datasets: UTD-MHAD, MM-Fit.
- Protocol highlights:
  - 3-second windows, 50% overlap.
  - inertial resampling to 50 Hz.
  - z-score normalization.
  - student model: transformer encoder with L=2, D=128, H=4.
  - KD settings: temperature T=3, alpha=0.7.
  - optimizer Adam, LR=1e-4, weight decay=1e-5, batch size 64, 20 epochs + early stopping.
- Reported results:
  - UTD-MHAD accuracy: 98.71%
  - MM-Fit accuracy: 98.55%

### Official Code Availability
- Official repo: https://github.com/Ism-ail11/XTinyHAR
- Required reference files to align with paper:
  - configs and preprocessing scripts
  - teacher/student training scripts
  - KD loss and patching logic

### Reproducibility Gaps / Ambiguities
- Dynamic patching details in paper text are richer than minimal fixed-patch ablation settings.
- Teacher implementation internals should be adopted from official code when available, not re-invented.

### WISDM Adaptation Rules
- Keep student-only inertial transformer path.
- WISDM input: `200 x 3` windows (20 Hz, 10 seconds).
- Default patch size for first pass: `P=20`.
- Mandatory variants:
  - `L=1, D=64, H=2`
  - `L=2, D=64, H=2`
  - `L=2, D=96, H=3`
- Optional ablation: dynamic patch policy proxy.

### Notebook Execution Checklist
- [ ] Log original paper facts and official code status.
- [ ] Train FP32 on WISDM (`random_stratified`, `user_holdout`).
- [ ] PTQ INT8 export + eval + deploy gate.
- [ ] QAT INT8 export + eval + deploy gate.
- [ ] Export per-protocol CSV/MD and append master table.

---

## Paper 2 — RepMobile
### Paper Facts (verbatim-verified)
- Citation: IEEE Sensors Journal (2024), DOI https://doi.org/10.1109/JSEN.2024.3424578
- Original datasets: PAMAP2, UniMiB-SHAR, WISDM, USC-HAD.
- Key paper/repo values:
  - structural reparameterization: multi-branch training-time blocks folded to plain inference graph.
  - data windows from repo preprocessing: WISDM=200, UniMiB=151, PAMAP2=342, USC-HAD=512.
  - overlap: 50% (per paper/repo preprocessing).
  - SGD optimizer, LR init `1e-4`, batch size `128`.
  - LR reduction by factor 2 per schedule (dataset dependent).
- Reported latency example on RPi4 (WISDM context): RepMobile ~43.91 ms vs MobileNet ~48.56 ms.

### Official Code Availability
- Official repo: https://github.com/Yuki0614/RepMobile
- Must confirm folding equivalence from code before WISDM-first TinyML export.

### Reproducibility Gaps / Ambiguities
- Some per-dataset split details are table-embedded and need explicit extraction into `paper_specs`.
- Need explicit numerical tolerance for pre-fold vs post-fold output equivalence.

### WISDM Adaptation Rules
- Use folded inference-time architecture for PTQ/QAT/export.
- Keep depthwise + pointwise structure quantization-friendly.
- Add explicit fold verification cell: max-abs-diff check on random batch.

### Notebook Execution Checklist
- [ ] Reparameterization equivalence check (pre-fold vs folded).
- [ ] FP32 WISDM train/eval on both split protocols.
- [ ] PTQ/QAT with strict INT8 I/O and deploy gate.
- [ ] Export results and update master report.

---

## Paper 3 — TCN-attention-HAR
### Paper Facts (verbatim-verified)
- Citation: Scientific Reports (2024), DOI https://doi.org/10.1038/s41598-024-57912-3
- Original datasets: WISDM, PAMAP2, USC-HAD.
- Protocol values reported:
  - window size 128, overlap 50%.
  - train:test = 8:2.
  - LR=0.0005, epochs=100.
  - multi-scale TCN kernels: 3, 5, 7 with dilated residual modules.
  - KD teacher/student variants (student CNN/LSTM/GRU).
- Reported examples:
  - WISDM teacher acc ~0.9903; student-CNN acc ~0.9927.

### Official Code Availability
- No official code repository declared in paper.
- Non-authoritative implementation for reference only:
  - https://github.com/zhuwei55555/TCN-attention-HAR

### Reproducibility Gaps / Ambiguities
- Attention head count contradiction: 8 listed in one section; 4 selected in tuning conclusion.
- KD coefficients (`alpha`, `beta`, `T`) should be mirrored from paper equations where explicit.

### WISDM Adaptation Rules
- WISDM-first implementation keeps multi-scale kernels 3/5/7.
- Primary config: `heads=4`; sanity comparison run: `heads=8`.
- Include lightweight student-only variant for MCU viability reporting.

### Notebook Execution Checklist
- [ ] Teacher + student WISDM runs.
- [ ] Heads=4 primary + heads=8 sanity run.
- [ ] PTQ/QAT strict deploy checks.
- [ ] Report teacher/student comparison and paper-delta notes.

---

## Paper 4 — Daghero et al. Quantized + Adaptive DNNs for MCUs
### Paper Facts (verbatim-verified)
- Citation: ACM TECS (2022), DOI https://doi.org/10.1145/3542819
- Original datasets: UniMiB-SHAR, UCI-HAPT, WISDM, WALK.
- Methodology highlights:
  - 1D CNN template search + QAT with PACT quantization.
  - fixed precisions explored: {8,4,2,1}.
  - mixed precision via EdMIPS-style differentiable search.
  - adaptive variable-width inference supports many runtime operating points.
- Reported deployment ranges include memory/latency/energy fronts; WISDM max reported F1 around 98.9 for top configs.

### Official Code Availability
- No single official end-to-end repo declared in paper.
- Toolchain context:
  - https://github.com/eml-eda/plinio
  - https://github.com/pulp-platform/dory
  - https://github.com/pulp-platform/pulp-nn

### Reproducibility Gaps / Ambiguities
- Sub-byte and mixed-precision flows are tightly coupled to original toolchain/hardware backend.
- Direct TFLite Micro equivalence for <8-bit paths is limited; deviations must be logged.

### WISDM Adaptation Rules
- WISDM-first pass implements:
  - 8-bit QAT/PTQ baseline.
  - mixed-precision proxy (software-level simulation/logging).
  - adaptive-width lite operating-mode sweep.
- Keep search-space subset tractable and reproducible in notebook.

### Notebook Execution Checklist
- [ ] CNN search-space subset run on WISDM.
- [ ] PTQ/QAT strict deploy checks.
- [ ] Adaptive-width lite frontier (accuracy vs cycles/complexity proxy).
- [ ] Clear note on what is proxy vs paper-native hardware pipeline.

---

## Paper 5 — TCN-Inception
### Paper Facts (verbatim-verified)
- Citation: Future Generation Computer Systems (2024), DOI https://doi.org/10.1016/j.future.2024.05.023
- Original datasets: UCI-HAR, MobiAct, Daphnet, DSADS.
- Core hyperparameters (paper table):
  - max kernel size (Inception): 68
  - bottleneck size: 32
  - TCN filters: 16
  - TCN kernel size: 3
  - dilation rates: (1, 2, 4, 8)
  - inception depth: 5
  - optimizer Adam, LR=0.0005, L2=0.01, epochs=300

### Official Code Availability
- No official repository declared in paper.

### Reproducibility Gaps / Ambiguities
- Exact split settings vary by dataset in paper; UCI-HAR explicitly uses random 70/30 in their setup section.
- Dataset-specific preprocessing is not uniformly implementation-detailed for all four datasets.

### WISDM Adaptation Rules
- Preserve architecture hyperparameters where feasible.
- Adapt input shape to WISDM accelerometer channels (`200 x 3`).
- Keep TCN dilation stack `(1,2,4,8)` and inception bottleneck path.

### Notebook Execution Checklist
- [ ] Build paper-like TCN-Inception with WISDM input adaptation.
- [ ] FP32/PTQ/QAT runs on both split protocols.
- [ ] Deploy-gate reporting and paper-target delta summary.

---

## WISDM-first standard protocol for all 5 notebooks
- Input: WISDM accelerometer only (`x,y,z`).
- Window: `200 x 3` (10 s at 20 Hz), unless a model-specific temporary override cell is enabled for ablation.
- Splits:
  - `random_stratified`
  - `user_holdout` (strict no-user-overlap)
- Metrics per run:
  - accuracy, macro-F1, classification report, confusion matrix
  - delegate-free TFLite op visibility (`interpreter_ops`, `interpreter_op_count`)
  - strict allowlist metadata (`allowed_ops_profile`, `allowed_ops_used`)
  - params count, `.tflite` size KB
  - PTQ/QAT status
  - deploy-gate flags (`full_integer_io`, `tflm_compatible`, unsupported ops)

## Mandatory notebook cell contract
1. Runtime guard + dependency checks.
2. Paper facts + code availability section.
3. WISDM preprocessing and adaptation section.
4. FP32 train/eval on both protocols.
5. PTQ INT8 export/eval.
6. QAT INT8 export/eval.
7. Deploy-gate summary.
8. Per-paper CSV/MD export + master table append.

## Output contracts
- Per paper:
  - `reports/<paper_slug>/<paper_slug>_results_<protocol>.csv`
  - `reports/<paper_slug>/<paper_slug>_summary.md`
- Master:
  - `reports/results_master.csv`
  - `reports/results_master.md`
  - include: `paper_target_score`, `delta_vs_paper`, `notes_assumptions`

## Required paper spec files
Create and maintain:
- `reports/paper_specs_xtinyhar.md`
- `reports/paper_specs_repmobile.md`
- `reports/paper_specs_tcn_attention_har.md`
- `reports/paper_specs_daghero_qadnn.md`
- `reports/paper_specs_tcn_inception.md`

Each file must include:
- citation + DOI
- code availability status
- original dataset protocol
- architecture/training settings
- target paper metrics
- WISDM adaptation mapping
- unresolved ambiguities + assumptions

## Validation and QA
- [ ] Unit tests for all 5 model builders (output shape and compile path).
- [ ] Split integrity tests for `user_holdout` (no leakage).
- [ ] Quant API tests for model-name-agnostic PTQ/QAT paths.
- [ ] Integration smoke runs (1 epoch) for all five notebooks.
- [ ] Reproducibility reruns (2 seeds/check repeats per model variant) with tolerance logging.
