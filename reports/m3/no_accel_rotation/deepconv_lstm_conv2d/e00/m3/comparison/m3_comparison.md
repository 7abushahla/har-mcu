# m3 Comparison

- Notes: M3 WISDM M2 anchor.

| pipeline | protocol | model | accuracy | macro_f1 | model_size_kb | training_time_sec | inference_latency_ms_median | inference_latency_ms_p95 | paper_target_accuracy | acc_delta_vs_target | ptq_status | qat_status | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WISDM replication | random_stratified | baseline float | 0.9881474978050921 | 0.9822859132186096 | 513.6171875 | 57.739019262 | — | — | — | — | ok | ok | ok |
| WISDM replication | random_stratified | PTQ int8 | 0.9796605209247878 | 0.9710121907893537 | 136.921875 | — | 4.25244199996655 | 4.303018000030079 | — | — | ok | — | ok |
| WISDM replication | random_stratified | QAT int8 | 0.8362598770851625 | 0.7908462432609756 | 137.34375 | 18.68213093600002 | 4.253262999981189 | 4.314031499959015 | — | — | — | ok | ok |
| paper target | — | baseline float | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | PTQ int8 | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | QAT int8 | — | — | — | — | — | — | — | — | — | — | reference |

