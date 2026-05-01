# m3 Comparison

- Notes: Train from scratch on Arduino train split and evaluate untouched Arduino test split.

| pipeline | protocol | model | accuracy | macro_f1 | model_size_kb | training_time_sec | inference_latency_ms_median | inference_latency_ms_p95 | paper_target_accuracy | acc_delta_vs_target | ptq_status | qat_status | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WISDM replication | random_stratified | baseline float | 0.9785082174462706 | 0.9784482389883088 | 1103.77734375 | 24.318561462999924 | — | — | — | — | failed | failed | ok |
| WISDM replication | random_stratified | PTQ int8 | 0.9778761061946902 | 0.9778175363348556 | 315.2109375 | — | 0.32039450002230296 | 0.34251099998527934 | — | — | failed | — | failed |
| WISDM replication | random_stratified | QAT int8 | 0.9791403286978508 | 0.9790974450851216 | 315.6796875 | 10.45778184300002 | 0.3273099999887563 | 0.3551734998836764 | — | — | — | failed | failed |
| paper target | — | baseline float | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | PTQ int8 | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | QAT int8 | — | — | — | — | — | — | — | — | — | — | reference |

