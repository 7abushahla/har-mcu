# daghero_qadnn Comparison

- Notes: Paper reports F1/MCU design fronts; direct WISDM accuracy target not fixed.

| pipeline | protocol | model | accuracy | macro_f1 | model_size_kb | training_time_sec | inference_latency_ms_median | inference_latency_ms_p95 | paper_target_accuracy | acc_delta_vs_target | ptq_status | qat_status | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WISDM replication | random_stratified | baseline float | 0.9930133657351154 | 0.9848455901863185 | 81.63671875 | 66.56295186700004 | — | — | — | — | ok | ok | ok |
| WISDM replication | random_stratified | PTQ int8 | 0.9939246658566221 | 0.9874841057833196 | 27.3671875 | — | 0.08982899998954963 | 0.10327649999908317 | — | — | ok | — | ok |
| WISDM replication | random_stratified | QAT int8 | 0.9924058323207776 | 0.9851424090002044 | 29.4140625 | 36.79993988199999 | 0.11571900006401847 | 0.14466575009919325 | — | — | — | ok | ok |
| WISDM replication | user_holdout | baseline float | 0.8208211143695014 | 0.7648593735898475 | 81.63671875 | 14.96201608499996 | — | — | — | — | ok | ok | ok |
| WISDM replication | user_holdout | PTQ int8 | 0.8234604105571848 | 0.7658416992159635 | 27.3671875 | — | 0.09025449992350332 | 0.10305900002549606 | — | — | ok | — | ok |
| WISDM replication | user_holdout | QAT int8 | 0.8598240469208212 | 0.8283029705525448 | 29.4140625 | 34.82446578600002 | 0.11503400003221032 | 0.12756124988300144 | — | — | — | ok | ok |
| paper target | — | baseline float | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | PTQ int8 | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | QAT int8 | — | — | — | — | — | — | — | — | — | — | reference |

