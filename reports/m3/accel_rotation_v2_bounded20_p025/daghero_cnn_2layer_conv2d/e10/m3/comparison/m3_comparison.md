# m3 Comparison

- Notes: Train from scratch on Arduino train split and evaluate untouched Arduino test split.

| pipeline | protocol | model | accuracy | macro_f1 | model_size_kb | training_time_sec | inference_latency_ms_median | inference_latency_ms_p95 | paper_target_accuracy | acc_delta_vs_target | ptq_status | qat_status | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WISDM replication | random_stratified | baseline float | 0.9924146649810367 | 0.9923863306358012 | 80.40625 | 14.110537843999964 | — | — | — | — | ok | ok | ok |
| WISDM replication | random_stratified | PTQ int8 | 0.9924146649810367 | 0.992387555619929 | 26.1328125 | — | 0.07478149996131833 | 0.0916067498906159 | — | — | ok | — | ok |
| WISDM replication | random_stratified | QAT int8 | 0.995575221238938 | 0.9955722315665388 | 26.734375 | 5.767861124999854 | 0.0753215000486307 | 0.09161199989193847 | — | — | — | ok | ok |
| paper target | — | baseline float | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | PTQ int8 | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | QAT int8 | — | — | — | — | — | — | — | — | — | — | reference |

