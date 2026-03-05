# TODOlistv3.md — TinyOL-First WISDM 6-Notebook Reproducibility Spec

## Scope and Locked Defaults
- Objective: implement TinyOL-related online-learning workflows in this codebase, with primary priority on reproducing the TinyOL paper pipeline and then extending to related methods.
- Dataset lock: WISDM accelerometer-only (`x,y,z`), `20 Hz`, `T=200` (10 seconds), `50% overlap`.
- Notebook scope lock (6):
  - `notebooks/replication_deepconvlstm.ipynb`
  - `notebooks/replication_daghero_qadnn.ipynb`
  - `notebooks/replication_repmobile.ipynb`
  - `notebooks/replication_tcn_attention_har.ipynb`
  - `notebooks/replication_tcn_inception.ipynb`
  - `notebooks/replication_xtinyhar.ipynb`
- Deployment target lock: Arduino Nano 33 BLE Sense (`256 KB SRAM`, `1 MB Flash`).
- Rollout lock:
  - Host-side TinyOL integration for all 6 notebooks first.
  - Full on-device validation initially required for 1 reference model.
- Acceptance lock: balanced numeric gate (functional + measurable adaptation gain + memory/latency/resource evidence).

## Priority Order
1. TinyOL (TinyML with Online-Learning on Microcontrollers, IJCNN 2021) end-to-end reproduction in this codebase.
2. Stabilize shared TinyOL abstractions and reporting for all six notebook variants.
3. Add extension tracks for SensOL, ODTL/few-shot personalization, and Dendron-style hierarchical task growth.

## Paper Evidence Matrix (Repo + Implementation + MCU Verified, 2026-03-05)
| Paper | Official Repo Status | Verified Repo / Code Links | Implementation Details to Reproduce (Paper + GitHub) | Deployed MCU/Platform in Paper | Key Numeric Targets |
|---|---|---|---|---|---|
| TinyOL: TinyML with Online-Learning on Microcontrollers (IJCNN 2021, DOI: 10.1109/IJCNN52387.2021.9533927) | No official repo declared | Paper/arXiv only; no official code link found | Add RAM-resident trainable output layer on frozen model; per-sample online update with SGD; running mean/variance normalization; optional class expansion (`add_class` behavior) | Arduino Nano 33 BLE Sense, Cortex-M4 @64 MHz, 256 KB SRAM | 2000 online updates; timing table around 1748 us inference vs 1921 us online iteration |
| TinyML on Microcontrollers... (ICSCN 2025, DOI: 10.1109/ICSCN67106.2025.11308574) | No official repo listed | Paper only; no official repo link found | Generic incremental engine (SGD/perceptron), micro-batching, sparse updates, fixed-point and duty-cycling strategy | STM32F746 (216 MHz, 512 KB RAM, 1 MB Flash) + Arduino Nano 33 BLE Sense (comparison setup) | HAR 88.3 -> 90.1; energy and latency reduction claims |
| SensOL: Memory-Efficient Online Learning for Tiny MCUs (IEEE SENSORS 2024, DOI: 10.1109/SENSORS60989.2024.10784905) | No official repo listed | Paper only; no official repo link found | TinyOL-style frozen backbone + online head; replay over latent exemplars; Int8 latent quantization + sparsity compression with masks; SGD on online layer; class-incremental expansion | STEVAL-STLKT01V1 kit with STM32L476JGY (Cortex-M4 @80 MHz, 128 KiB SRAM, 1028 KiB Flash) | 115x exemplar memory reduction; update step ~1 ms; SHL class-incremental protocol |
| On-Device Training Empowered Transfer Learning for HAR (arXiv:2407.03644) | No explicit official repo link in paper text | Companion repo (author-linked, not explicitly cited as official): `https://github.com/kangpx/onlineTiny2023` | Residual 1D-CNN backbone + single dense classifier; freeze backbone; per-sample dense-layer update with SGD+momentum/EMA; STM32 engine (classifier in SRAM, backbone in Flash), GAP9 engine (L2/L1 DMA + parallel update kernels) | NUCLEO-F756ZG (STM32F756ZG) and GAP9 | Mean gains +3.73 / +17.38 / +3.70; GAP9 reported 20x lower latency and 280x lower power vs STM32F7 during ODTL |
| Dendron: Enhancing HAR with On-Device TinyML Learning (IEEE CIES 2025, DOI: 10.1109/CIES64955.2025.11007628) | No official repo listed | Paper only; no official repo link found | Shared feature extractor `g(.)` + multiple task FC heads `h(i)`; dependency matrix `D`; unified multi-output off-device training; on-device learning of only new FC head + schema update algorithm | STM32-NUCLEO-F401RE | 5x less memory, 2x less compute/latency vs hierarchical baseline; reported on-device learning timing for new task |
| Bridging Generalization and Personalization in HAR via On-Device Few-Shot Learning (arXiv:2508.15413) | Official repo linked by paper | `https://github.com/kangpx/onlineTiny2023` | Frozen backbone + trainable dense classifier; few-shot per-sample updates; GAP9 runtime engine with classifier updates and low-overhead memory movement; repo includes `model-zoo`, `on_line_training.py`, STM32 and GAP9 deployment paths | GAP9 (RISC-V) | RecGym/QVAR/Ultra gains +3.73/+17.38/+3.70; ~0.34 ms inference, ~0.94 ms update, microjoule-level update energy |

## GitHub Verification Ledger (TinyOL Track)
- Verification date: `2026-03-05`
- TinyOL (IJCNN 2021): no official repo link in paper/arXiv.
- ICSCN 2025 incremental TinyML: no official repo link in paper text.
- SensOL 2024: no official repo link in paper text.
- ODTL 2024: no explicit official code link; treat `onlineTiny2023` as companion, not official.
- Dendron 2025: no official repo link in paper text.
- Few-shot 2025: official repo explicitly linked to `onlineTiny2023`.

### Companion/Official Repo Extraction Tasks (`onlineTiny2023`)
- [ ] Extract exact model topology used in ODTL/few-shot runs (backbone + dense head dimensions).
- [ ] Extract on-device update routine details from `on_line_training.py` and deployment folders.
- [ ] Extract platform-specific runtime flow for `stm32_nucleo_f756zg` and `greenwaves_gap9`.
- [ ] Map repository configuration knobs to planned `tinyol.*` config schema in this codebase.

## Documentation Schema Additions for Paper Rows
- No code API change in this step.
- Add documentation schema fields inside TODO tracking for every paper row:
  - `repo_status`
  - `repo_links`
  - `repo_relation` (`official` | `companion` | `none`)
  - `repo_verified_date`
  - `paper_mcu_platform`
  - `paper_mcu_specs`
  - `paper_impl_details`
  - `github_impl_details`
- Keep existing `tinyol.*`, `sensol.*`, `odtl.*`, `dendron.*` planning keys unchanged.

## Paper Extraction Ledger Requirements
- Extract and document for each of the 6 TinyOL-related papers:
  - citation, DOI/arXiv ID, venue/year
  - official code status and link verification date
  - dataset/protocol details (windowing, sampling rate, train/test split policy)
  - architecture details (frozen/trainable parts, update equations, optimizer)
  - deployment hardware details and timing/energy/memory claims
  - exact reported main metrics used for comparison
  - reproducibility gaps and assumptions needed for WISDM mapping
- Maintain a strict distinction between:
  - paper-native metrics
  - WISDM adaptation metrics

## TinyOL-First Milestone Plan (Must Work Before Extensions)
- M1 objective: produce TinyOL online adaptation runs for all six notebook-derived model paths on WISDM in host simulation mode.
- Minimum TinyOL pipeline contract:
  - frozen backbone embedding/extractor path
  - online trainable head initialized in RAM-equivalent data structure
  - per-sample prediction + optional supervised update
  - adaptation stream split separated from evaluation stream
  - pre-adaptation and post-adaptation metrics in one standardized artifact
- Required M1 outputs:
  - one TinyOL result JSON/MD artifact per model variant per split protocol
  - unified tinyol master table for the 6 models
  - adaptation curve plot and online-update timing summary per run

## Codebase Setup Scripts Plan
- Create/setup script tasks for TinyOL workflow bootstrap:
  - generate TinyOL config stubs for each notebook/model variant
  - clone notebook templates to TinyOL-specific notebook variants
  - create TinyOL report directory scaffolding
  - emit paper evidence matrix template and per-paper extraction templates
- Use deterministic naming contracts for TinyOL outputs:
  - `reports/tinyol/<model_slug>/...`
  - `reports/tinyol_specs/...`
  - `configs/tinyol/<model_slug>_tinyol_wisdm.yaml`

## Core Online-Learning Abstraction Plan
- Add a shared TinyOL algorithm interface in `src/tinyol` with fixed entrypoints:
  - `predict(...)`
  - `online_update(...)`
  - `reset(...)`
  - optional `add_class(...)`
- Define common runtime state structures:
  - online head parameters
  - optimizer state (if used, e.g., momentum/EMA)
  - class metadata and optional expandable class map
  - stream counters and timing accumulators
- Add a memory-estimation helper for deployment planning:
  - static model footprint
  - online state footprint
  - update workspace estimate
  - safety margin against Nano 33 BLE Sense SRAM/Flash limits

## TinyOL Config and Schema Additions
- Add standardized config namespace under `tinyol.*`:
  - `tinyol.algorithm_variant`
  - `tinyol.online_lr`
  - `tinyol.update_budget_k`
  - `tinyol.stream_protocol`
  - `tinyol.adaptation_eval_split`
  - `tinyol.enable_class_expansion`
- Add optional extension config namespaces:
  - `sensol.*` for replay/compression
  - `odtl.*` for momentum/EMA update behavior
  - `dendron.*` for hierarchical task schema rules
- Backward compatibility rule:
  - append new fields to existing report payloads
  - do not rename/remove existing non-TinyOL report keys

## Per-Notebook TinyOL Integration Checklist (Host-Side First)
- For each of the 6 notebooks:
  - [ ] add TinyOL method intro cell with source paper traceability
  - [ ] reuse WISDM preprocessing at `T=200`, `20 Hz`, `50% overlap`
  - [ ] export frozen-feature stream for online adaptation
  - [ ] run pre-adaptation evaluation on `random_stratified` and `user_holdout`
  - [ ] run online adaptation stream with fixed `K` schedule
  - [ ] run post-adaptation evaluation
  - [ ] save TinyOL metrics payload + adaptation curve + timing summary
  - [ ] append row to TinyOL master comparison artifact

## MCU Deployment Crosswalk (Paper Hardware vs Project Target)
| Paper | Paper MCU/Platform | Relevance to Nano 33 BLE Sense |
|---|---|---|
| TinyOL | Arduino Nano 33 BLE Sense (Cortex-M4, 256 KB SRAM) | Directly aligned; primary baseline for first on-device reproduction |
| ICSCN 2025 | STM32F746 + Arduino Nano 33 BLE Sense | Partial alignment; use as contextual incremental-learning baseline |
| SensOL | STM32L476JGY (Cortex-M4, 128 KiB SRAM) | Useful low-memory reference; replay/compression strategy relevant |
| ODTL | STM32F756ZG + GAP9 | Method transferable; hardware acceleration assumptions must be isolated |
| Dendron | STM32-NUCLEO-F401RE | Useful hierarchical/on-device-head-learning reference under constrained MCU |
| Few-shot | GAP9 | Personalization pipeline relevant; latency/energy targets not directly portable to Nano |

## Hardware Milestone Checklist (Reference Model First)
- Reference model default: DeepConvLSTM TinyOL path (existing simulator/deploy path already present in repo).
- Required on-device validation tasks:
  - [ ] compile and flash TinyOL reference firmware on Nano 33 BLE Sense
  - [ ] verify tensor arena and memory-fit margins
  - [ ] measure inference-only latency and update-enabled latency
  - [ ] execute repeated online updates (`>=2000`) without runtime failure
  - [ ] collect and store timing/resource logs in reproducible artifacts
  - [ ] validate adaptation gain evidence reported from controlled stream

## Extension Tracks (After TinyOL Baseline Pass)
- SensOL track:
  - replay buffer design
  - int8 latent exemplar storage
  - sparsity compression/decompression utilities
  - replay refresh schedule evaluation
- ODTL/few-shot track:
  - classifier-only SGD+momentum/EMA updates
  - user personalization protocol and budgeted few-shot runs
- Dendron track:
  - shared feature extractor + task-specific heads
  - dependency schema for incremental task integration
  - low-data new-task onboarding analysis

## Output Contracts
- TinyOL run artifacts (per model, per protocol):
  - `pre_adapt_accuracy`
  - `post_adapt_accuracy`
  - `pre_adapt_macro_f1`
  - `post_adapt_macro_f1`
  - `delta_accuracy`
  - `delta_macro_f1`
  - `online_update_time_mean_us`
  - `online_update_time_p95_us`
  - `online_steps`
  - `memory_estimate_bytes`
- Additional optional blocks:
  - `sensol` block (replay/compression metrics)
  - `odtl` block (momentum/EMA settings and stats)
  - `dendron` block (hierarchical schema metadata)
- Master outputs:
  - `reports/tinyol/tinyol_results_master.csv`
  - `reports/tinyol/tinyol_results_master.md`
  - per-paper extraction docs under `reports/tinyol_specs/`

## Required Paper Spec Files
- Create and maintain:
  - `reports/tinyol_specs/paper_spec_tinyol.md`
  - `reports/tinyol_specs/paper_spec_tinyml_incremental_icscn2025.md`
  - `reports/tinyol_specs/paper_spec_sensol.md`
  - `reports/tinyol_specs/paper_spec_odtl_har.md`
  - `reports/tinyol_specs/paper_spec_dendron.md`
  - `reports/tinyol_specs/paper_spec_fewshot_personalization.md`
- Each file must include:
  - citation and DOI/arXiv
  - code availability status
  - original protocol/dataset
  - architecture and update-rule details
  - target paper metrics
  - WISDM adaptation mapping
  - unresolved ambiguities and explicit assumptions

## Validation and QA
- Doc QA for this TinyOL repo/MCU update:
  - [ ] matrix completeness: each of 6 paper rows has repo status, implementation details, and MCU field
  - [ ] repo policy consistency: ODTL row marked companion (not official), few-shot row marked official
  - [ ] link integrity: DOI/arXiv/GitHub links are valid
  - [ ] no priority drift: TinyOL remains first milestone and first hardware validation basis
  - [ ] no scope drift: WISDM + 6 notebooks + Nano 33 BLE Sense constraints unchanged
- Unit tests:
  - [ ] TinyOL softmax/logistic per-sample updates versus NumPy reference.
  - [ ] class expansion path initializes new class parameters correctly.
  - [ ] SensOL-style replay compression/decompression invariants.
  - [ ] memory budget estimator respects Nano 33 BLE Sense SRAM/Flash bounds.
- Integration tests:
  - [ ] smoke run for all six TinyOL notebooks in reduced mode.
  - [ ] artifact schema checks for required TinyOL fields.
  - [ ] regression checks: existing non-TinyOL paper pipeline unchanged when TinyOL disabled.
- Hardware-adjacent checks:
  - [ ] reference-model repeated-update stress test (`>=2000`) with timing logs.

## Milestones and Acceptance Gates
### M1 — TinyOL Core (Highest Priority)
- Host-side TinyOL adaptation implemented and reported for all 6 notebook-derived TinyOL pipelines.
- Required gate:
  - measurable adaptation gain on `user_holdout` in aggregate across model set
  - complete standardized TinyOL artifacts for each model/protocol

### M2 — TinyOL On-Device Reference
- One reference model validated on Arduino Nano 33 BLE Sense with memory-fit and timing evidence.
- Required gate:
  - sustained online updates complete without runtime failure
  - inference and update timing logs are captured and stored

### M3 — Other TinyOL Techniques
- SensOL, ODTL/few-shot, and Dendron tracks added as explicit experimental branches after M1 pass.

### Balanced Numeric Gate (M1 + M2)
- Adaptation gain must be measurable on `user_holdout` with per-model deltas reported.
- At least one on-device reference path must complete sustained online updates within board constraints.
- All runs must publish memory, latency, and resource evidence in addition to accuracy metrics.

## Explicit Assumptions and Defaults
- Default first hardware reference remains DeepConvLSTM TinyOL path due existing simulator/deploy support in this repository.
- Default repo policy selected: ODTL uses `onlineTiny2023` as companion, not official.
- If no explicit repo URL exists in paper/arXiv metadata, status remains `no official repo`.
- WISDM-first adaptation is mandatory, even for papers originally evaluated on non-WISDM datasets.
- Papers without official implementation repositories are reproduced via method-faithful approximations, and all assumptions are explicitly logged.
- The ICSCN 2025 incremental TinyML paper is treated as contextual/supportive and does not override TinyOL-first implementation priority.
- MCU evidence is paper-declared deployment hardware only; portability to Nano is tracked separately.

## Sources to Cite in TinyOL Paper Specs
- TinyOL arXiv: https://arxiv.org/abs/2103.08295
- ODTL arXiv: https://arxiv.org/abs/2407.03644
- Few-shot arXiv: https://arxiv.org/abs/2508.15413
- Few-shot/companion repo: https://github.com/kangpx/onlineTiny2023
- TinyOL DOI: https://doi.org/10.1109/IJCNN52387.2021.9533927
- ICSCN DOI: https://doi.org/10.1109/ICSCN67106.2025.11308574
- SensOL DOI: https://doi.org/10.1109/SENSORS60989.2024.10784905
- Dendron DOI: https://doi.org/10.1109/CIES64955.2025.11007628
