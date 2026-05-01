# m3 Comparison

- Notes: M3 WISDM M2 anchor.

| pipeline | protocol | model | accuracy | macro_f1 | model_size_kb | training_time_sec | inference_latency_ms_median | inference_latency_ms_p95 | paper_target_accuracy | acc_delta_vs_target | ptq_status | qat_status | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WISDM replication | random_stratified | baseline float | 0.9416154521510096 | 0.915202284250101 | 93.3828125 | 42.616925985999984 | — | — | — | — | ok | ok | ok |
| WISDM replication | random_stratified | PTQ int8 | 0.9417617793386011 | 0.9147946364819458 | 42.125 | — | 0.3258505000189871 | 0.354818249974187 | — | — | ok | — | ok |
| WISDM replication | random_stratified | QAT int8 | 0.9536142815335089 | 0.9340028169212138 | 43.2578125 | 25.396587339999996 | 0.32731999999668915 | 0.36691600001859115 | — | — | — | ok | ok |
| paper target | — | baseline float | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | PTQ int8 | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | QAT int8 | — | — | — | — | — | — | — | — | — | — | reference |

