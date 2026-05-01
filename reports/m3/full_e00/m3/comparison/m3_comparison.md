# m3 Comparison

- Notes: M3 WISDM M2 anchor.

| pipeline | protocol | model | accuracy | macro_f1 | model_size_kb | training_time_sec | inference_latency_ms_median | inference_latency_ms_p95 | paper_target_accuracy | acc_delta_vs_target | ptq_status | qat_status | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WISDM replication | random_stratified | baseline float | 0.9884401521802751 | 0.9831177999390307 | 513.6171875 | 56.28332130199999 | — | — | — | — | ok | ok | ok |
| WISDM replication | random_stratified | PTQ int8 | 0.9800995024875622 | 0.9713485385927911 | 136.921875 | — | 4.251617999983637 | 4.33369924999738 | — | — | ok | — | ok |
| WISDM replication | random_stratified | QAT int8 | 0.8238220661398888 | 0.7751120983264624 | 137.34375 | 18.306112369000004 | 4.246367000007467 | 4.332625749967178 | — | — | — | ok | ok |
| paper target | — | baseline float | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | PTQ int8 | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | QAT int8 | — | — | — | — | — | — | — | — | — | — | reference |

