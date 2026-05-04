# m3 Comparison

- Notes: M3 WISDM M2 anchor.

| pipeline | protocol | model | accuracy | macro_f1 | model_size_kb | training_time_sec | inference_latency_ms_median | inference_latency_ms_p95 | paper_target_accuracy | acc_delta_vs_target | ptq_status | qat_status | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WISDM replication | random_stratified | baseline float | 0.9922446590576529 | 0.9894639736959916 | 80.40625 | 41.407536686000014 | — | — | — | — | ok | ok | ok |
| WISDM replication | random_stratified | PTQ int8 | 0.99195200468247 | 0.9892684421310998 | 26.1328125 | — | 0.07530650000830974 | 0.09158225000760467 | — | — | ok | — | ok |
| WISDM replication | random_stratified | QAT int8 | 0.9934152765583846 | 0.9907973930721491 | 26.734375 | 15.453625466999995 | 0.07584650001035698 | 0.0989747500170779 | — | — | — | ok | ok |
| paper target | — | baseline float | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | PTQ int8 | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | QAT int8 | — | — | — | — | — | — | — | — | — | — | reference |

