# m3 Comparison

- Notes: Same protocol as E10 (train from scratch on Arduino train, eval Arduino test, train_zscore) but T=50 (2.5 s @ 20 Hz). Compare to E10 (T=100) for window-length apples-to-apples.

| pipeline | protocol | model | accuracy | macro_f1 | model_size_kb | training_time_sec | inference_latency_ms_median | inference_latency_ms_p95 | paper_target_accuracy | acc_delta_vs_target | ptq_status | qat_status | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WISDM replication | random_stratified | baseline float | 0.9807570977917981 | 0.980791308380784 | 396.4296875 | 28.520658929000092 | — | — | — | — | ok | ok | ok |
| WISDM replication | random_stratified | PTQ int8 | 0.9482649842271293 | 0.9485755497515967 | 107.625 | — | 2.0401400000764625 | 2.084650000028887 | — | — | ok | — | ok |
| WISDM replication | random_stratified | QAT int8 | 0.7962145110410095 | 0.8012452304358938 | 108.046875 | 10.161367962999975 | 2.039310499981184 | 2.067950999958157 | — | — | — | ok | ok |
| paper target | — | baseline float | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | PTQ int8 | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | QAT int8 | — | — | — | — | — | — | — | — | — | — | reference |

