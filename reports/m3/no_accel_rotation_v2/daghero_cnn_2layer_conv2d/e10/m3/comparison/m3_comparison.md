# m3 Comparison

- Notes: Train from scratch on Arduino train split and evaluate untouched Arduino test split.

| pipeline | protocol | model | accuracy | macro_f1 | model_size_kb | training_time_sec | inference_latency_ms_median | inference_latency_ms_p95 | paper_target_accuracy | acc_delta_vs_target | ptq_status | qat_status | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WISDM replication | random_stratified | baseline float | 0.9949431099873578 | 0.9949349373380407 | 80.40625 | 12.739101772999902 | — | — | — | — | ok | ok | ok |
| WISDM replication | random_stratified | PTQ int8 | 0.9943109987357776 | 0.9943036699161943 | 26.1328125 | — | 0.07488699998248194 | 0.09147949998578042 | — | — | ok | — | ok |
| WISDM replication | random_stratified | QAT int8 | 0.995575221238938 | 0.9955735157931862 | 26.734375 | 5.378131107999934 | 0.0754164998397755 | 0.09189199994352748 | — | — | — | ok | ok |
| paper target | — | baseline float | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | PTQ int8 | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | QAT int8 | — | — | — | — | — | — | — | — | — | — | reference |

