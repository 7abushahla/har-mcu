# m3 Comparison

- Notes: Train from scratch on Arduino train split and evaluate untouched Arduino test split.

| pipeline | protocol | model | accuracy | macro_f1 | model_size_kb | training_time_sec | inference_latency_ms_median | inference_latency_ms_p95 | paper_target_accuracy | acc_delta_vs_target | ptq_status | qat_status | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WISDM replication | random_stratified | baseline float | 0.993046776232617 | 0.9930530983042587 | 1883.359375 | 33.40089521200025 | — | — | — | — | ok | ok | ok |
| WISDM replication | random_stratified | PTQ int8 | 0.9924146649810367 | 0.9924217149714668 | 578.3984375 | — | 8.054503000039404 | 8.357202499837513 | — | — | ok | — | ok |
| WISDM replication | random_stratified | QAT int8 | 0.9936788874841972 | 0.9936819405964957 | 585.59375 | 28.79973711399998 | 8.099148999917816 | 8.198238499971922 | — | — | — | ok | ok |
| paper target | — | baseline float | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | PTQ int8 | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | QAT int8 | — | — | — | — | — | — | — | — | — | — | reference |

