# m3 Comparison

- Notes: M3 WISDM M2 anchor.

| pipeline | protocol | model | accuracy | macro_f1 | model_size_kb | training_time_sec | inference_latency_ms_median | inference_latency_ms_p95 | paper_target_accuracy | acc_delta_vs_target | ptq_status | qat_status | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WISDM replication | random_stratified | baseline float | 0.9920983318700615 | 0.9893811078113246 | 80.40625 | 36.996624198000006 | — | — | — | — | ok | ok | ok |
| WISDM replication | random_stratified | PTQ int8 | 0.9920983318700615 | 0.9892397696568799 | 26.1328125 | — | 0.07530899998187124 | 0.09082750000288797 | — | — | ok | — | ok |
| WISDM replication | random_stratified | QAT int8 | 0.9929762949956101 | 0.9901445558676766 | 26.734375 | 13.46329293599996 | 0.07503499998051666 | 0.09245575000704775 | — | — | — | ok | ok |
| paper target | — | baseline float | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | PTQ int8 | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | QAT int8 | — | — | — | — | — | — | — | — | — | — | reference |

