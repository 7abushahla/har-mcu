# m3 Comparison

- Notes: M3 WISDM M2 anchor.

| pipeline | protocol | model | accuracy | macro_f1 | model_size_kb | training_time_sec | inference_latency_ms_median | inference_latency_ms_p95 | paper_target_accuracy | acc_delta_vs_target | ptq_status | qat_status | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WISDM replication | random_stratified | baseline float | 0.9569798068481123 | 0.9442987986633135 | 1103.77734375 | 80.48402849200002 | — | — | — | — | failed | failed | ok |
| WISDM replication | random_stratified | PTQ int8 | 0.9562481709101551 | 0.9435157979013424 | 315.2109375 | — | 0.32084450000979814 | 0.3415525000178832 | — | — | failed | — | failed |
| WISDM replication | random_stratified | QAT int8 | 0.9615159496634474 | 0.9493589080627994 | 315.6796875 | 28.375500330000023 | 0.3236189999995531 | 0.36213850000876846 | — | — | — | failed | failed |
| paper target | — | baseline float | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | PTQ int8 | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | QAT int8 | — | — | — | — | — | — | — | — | — | — | reference |

