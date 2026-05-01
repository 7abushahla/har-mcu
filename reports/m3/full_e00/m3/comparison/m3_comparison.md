# m3 Comparison

- Notes: M3 WISDM M2 anchor.

| pipeline | protocol | model | accuracy | macro_f1 | model_size_kb | training_time_sec | inference_latency_ms_median | inference_latency_ms_p95 | paper_target_accuracy | acc_delta_vs_target | ptq_status | qat_status | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WISDM replication | random_stratified | baseline float | 0.9885864793678666 | 0.9832806154804284 | 513.6171875 | 57.95538895300001 | — | — | — | — | ok | ok | ok |
| WISDM replication | random_stratified | PTQ int8 | 0.9802458296751536 | 0.9719087901072831 | 136.921875 | — | 4.245099499996741 | 4.324175749999881 | — | — | ok | — | ok |
| WISDM replication | random_stratified | QAT int8 | 0.8187006145741879 | 0.7736428461876698 | 137.34375 | 18.593344601999945 | 4.250589000008631 | 4.3484310000252435 | — | — | — | ok | ok |
| paper target | — | baseline float | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | PTQ int8 | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | QAT int8 | — | — | — | — | — | — | — | — | — | — | reference |
