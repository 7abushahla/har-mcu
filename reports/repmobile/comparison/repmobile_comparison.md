# repmobile Comparison

- Notes: Paper emphasizes latency and efficiency; WISDM adaptation target accuracy not fixed here.

| pipeline | protocol | model | accuracy | macro_f1 | model_size_kb | training_time_sec | inference_latency_ms_median | inference_latency_ms_p95 | paper_target_accuracy | acc_delta_vs_target | ptq_status | qat_status | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WISDM replication | random_stratified | baseline float | 0.7715674362089915 | 0.577059167353506 | 94.68359375 | 19.76040043499961 | — | — | — | — | ok | ok | ok |
| WISDM replication | random_stratified | PTQ int8 | 0.7688335358444714 | 0.5744658932531931 | 43.4140625 | — | 0.4126460000861698 | 0.4808159999356576 | — | — | ok | — | ok |
| WISDM replication | random_stratified | QAT int8 | 0.807411907654921 | 0.6037255503044259 | 46.9140625 | 18.618353685999864 | 0.5283049999889045 | 0.5476575000784578 | — | — | — | ok | ok |
| WISDM replication | user_holdout | baseline float | 0.7372434017595307 | 0.5323846994461402 | 94.68359375 | 17.628862212999593 | — | — | — | — | ok | ok | ok |
| WISDM replication | user_holdout | PTQ int8 | 0.7284457478005865 | 0.5315173051412764 | 43.4140625 | — | 0.41620100023465056 | 0.465745749920643 | — | — | ok | — | ok |
| WISDM replication | user_holdout | QAT int8 | 0.7621700879765396 | 0.5156669176716828 | 46.9140625 | 18.730120572999567 | 0.5446200000278623 | 0.5960000000868604 | — | — | — | ok | ok |
| paper target | — | baseline float | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | PTQ int8 | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | QAT int8 | — | — | — | — | — | — | — | — | — | — | reference |

