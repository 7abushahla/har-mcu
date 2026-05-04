# m3 Comparison

- Notes: M3 WISDM M2 anchor.

| pipeline | protocol | model | accuracy | macro_f1 | model_size_kb | training_time_sec | inference_latency_ms_median | inference_latency_ms_p95 | paper_target_accuracy | acc_delta_vs_target | ptq_status | qat_status | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WISDM replication | random_stratified | baseline float | 0.9938542581211589 | 0.9915268142182478 | 80.40625 | 36.446077409 | — | — | — | — | ok | ok | ok |
| WISDM replication | random_stratified | PTQ int8 | 0.993561603745976 | 0.9911763261221543 | 26.1328125 | — | 0.07819600000402716 | 0.09506700000372348 | — | — | ok | — | ok |
| WISDM replication | random_stratified | QAT int8 | 0.9944395668715247 | 0.9923854766083867 | 26.734375 | 13.385450649999996 | 0.07507099999770617 | 0.09150449999140164 | — | — | — | ok | ok |
| paper target | — | baseline float | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | PTQ int8 | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | QAT int8 | — | — | — | — | — | — | — | — | — | — | reference |

