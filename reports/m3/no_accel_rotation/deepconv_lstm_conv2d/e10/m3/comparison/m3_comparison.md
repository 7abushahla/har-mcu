# m3 Comparison

- Notes: Train from scratch on Arduino train split and evaluate untouched Arduino test split.

| pipeline | protocol | model | accuracy | macro_f1 | model_size_kb | training_time_sec | inference_latency_ms_median | inference_latency_ms_p95 | paper_target_accuracy | acc_delta_vs_target | ptq_status | qat_status | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WISDM replication | random_stratified | baseline float | 0.9879898862199747 | 0.9880019558727158 | 513.6171875 | 11.874945432999993 | — | — | — | — | ok | ok | ok |
| WISDM replication | random_stratified | PTQ int8 | 0.9399494310998736 | 0.9416830034455206 | 136.921875 | — | 4.248584500032848 | 4.291977500088251 | — | — | ok | — | ok |
| WISDM replication | random_stratified | QAT int8 | 0.3647281921618205 | 0.34106181274095554 | 137.34375 | 6.6810593729999255 | 4.251025000030495 | 4.285953249961949 | — | — | — | ok | ok |
| paper target | — | baseline float | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | PTQ int8 | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | QAT int8 | — | — | — | — | — | — | — | — | — | — | reference |

