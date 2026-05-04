# m3 Comparison

- Notes: M3 WISDM M2 anchor.

| pipeline | protocol | model | accuracy | macro_f1 | model_size_kb | training_time_sec | inference_latency_ms_median | inference_latency_ms_p95 | paper_target_accuracy | acc_delta_vs_target | ptq_status | qat_status | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WISDM replication | random_stratified | baseline float | 0.9869768803043606 | 0.9827565499865419 | 513.6171875 | 70.888669096 | — | — | — | — | ok | ok | ok |
| WISDM replication | random_stratified | PTQ int8 | 0.9435177055896986 | 0.8862849007246557 | 136.921875 | — | 4.243880500041541 | 4.302985999984799 | — | — | ok | — | ok |
| WISDM replication | random_stratified | QAT int8 | 0.43195785776997364 | 0.3072657023863392 | 137.34375 | 20.712699843999985 | 4.251294999988886 | 4.304881999999566 | — | — | — | ok | ok |
| paper target | — | baseline float | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | PTQ int8 | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | QAT int8 | — | — | — | — | — | — | — | — | — | — | reference |

