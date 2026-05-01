# m3 Comparison

- Notes: M3 WISDM M2 anchor.

| pipeline | protocol | model | accuracy | macro_f1 | model_size_kb | training_time_sec | inference_latency_ms_median | inference_latency_ms_p95 | paper_target_accuracy | acc_delta_vs_target | ptq_status | qat_status | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WISDM replication | random_stratified | baseline float | 0.9942932396839332 | 0.9915117203094934 | 1883.359375 | 161.581134272 | — | — | — | — | ok | ok | ok |
| WISDM replication | random_stratified | PTQ int8 | 0.9938542581211589 | 0.9908532082374902 | 578.3984375 | — | 8.258283499998242 | 8.572420999996666 | — | — | ok | — | ok |
| WISDM replication | random_stratified | QAT int8 | 0.9950248756218906 | 0.9925260256072522 | 585.59375 | 91.73268636599994 | 8.317568999984815 | 8.644121749995293 | — | — | — | ok | ok |
| paper target | — | baseline float | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | PTQ int8 | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | QAT int8 | — | — | — | — | — | — | — | — | — | — | reference |

