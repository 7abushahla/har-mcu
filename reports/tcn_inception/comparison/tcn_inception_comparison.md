# tcn_inception Comparison

- Notes: Paper targets are on other datasets; WISDM entries are adaptation results.

| pipeline | protocol | model | accuracy | macro_f1 | model_size_kb | training_time_sec | inference_latency_ms_median | inference_latency_ms_p95 | paper_target_accuracy | acc_delta_vs_target | ptq_status | qat_status | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WISDM replication | random_stratified | baseline float | 0.9975698663426489 | 0.9946249801470524 | 1331.265625 | 112.29065538499981 | — | — | — | — | ok | ok | ok |
| WISDM replication | random_stratified | PTQ int8 | 0.9975698663426489 | 0.9946249801470524 | 379.4453125 | — | 3.013092999935907 | 3.0557055001736444 | — | — | ok | — | ok |
| WISDM replication | random_stratified | QAT int8 | 0.99726609963548 | 0.9941675641266796 | 384.8125 | 126.28274708799972 | 3.203451000217683 | 3.2976932500332623 | — | — | — | ok | ok |
| WISDM replication | user_holdout | baseline float | 0.8149560117302053 | 0.7430573804582373 | 1331.265625 | 48.31784683199976 | — | — | — | — | ok | ok | ok |
| WISDM replication | user_holdout | PTQ int8 | 0.8137829912023461 | 0.7434444357808547 | 379.4453125 | — | 3.0616479998570867 | 3.159566250133139 | — | — | ok | — | ok |
| WISDM replication | user_holdout | QAT int8 | 0.843108504398827 | 0.8026200678492138 | 384.8125 | 126.98800381700039 | 3.268084999490384 | 3.333332500005781 | — | — | — | ok | ok |
| paper target | — | baseline float | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | PTQ int8 | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | QAT int8 | — | — | — | — | — | — | — | — | — | — | reference |

