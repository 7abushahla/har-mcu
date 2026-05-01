# m3 Comparison

- Notes: Same protocol as E10 (train from scratch on Arduino train, eval Arduino test, train_zscore) but T=50 (2.5 s @ 20 Hz). Compare to E10 (T=100) for window-length apples-to-apples.

| pipeline | protocol | model | accuracy | macro_f1 | model_size_kb | training_time_sec | inference_latency_ms_median | inference_latency_ms_p95 | paper_target_accuracy | acc_delta_vs_target | ptq_status | qat_status | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WISDM replication | random_stratified | baseline float | 0.9867507886435332 | 0.9867634493004028 | 1322.98828125 | 29.399675242000058 | — | — | — | — | ok | ok | ok |
| WISDM replication | random_stratified | PTQ int8 | 0.9867507886435332 | 0.9867649890120638 | 369.921875 | — | 1.3010189999818067 | 1.3209922500152516 | — | — | ok | — | ok |
| WISDM replication | random_stratified | QAT int8 | 0.9876971608832807 | 0.987713005412703 | 378.375 | 39.05522768499998 | 1.373974500040731 | 1.3936249999915162 | — | — | — | ok | ok |
| paper target | — | baseline float | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | PTQ int8 | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | QAT int8 | — | — | — | — | — | — | — | — | — | — | reference |

