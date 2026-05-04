# m3 Comparison

- Notes: Train from scratch on Arduino train split and evaluate untouched Arduino test split.

| pipeline | protocol | model | accuracy | macro_f1 | model_size_kb | training_time_sec | inference_latency_ms_median | inference_latency_ms_p95 | paper_target_accuracy | acc_delta_vs_target | ptq_status | qat_status | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WISDM replication | random_stratified | baseline float | 0.9911504424778761 | 0.991148404724707 | 513.6171875 | 17.43070001199999 | — | — | — | — | ok | ok | ok |
| WISDM replication | random_stratified | PTQ int8 | 0.9506953223767383 | 0.9517390327054853 | 136.921875 | — | 4.246705500008829 | 4.300248499987447 | — | — | ok | — | ok |
| WISDM replication | random_stratified | QAT int8 | 0.44563843236409606 | 0.455699901430644 | 137.34375 | 7.3892535029999635 | 4.248145499900602 | 4.307880999988356 | — | — | — | ok | ok |
| paper target | — | baseline float | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | PTQ int8 | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | QAT int8 | — | — | — | — | — | — | — | — | — | — | reference |

