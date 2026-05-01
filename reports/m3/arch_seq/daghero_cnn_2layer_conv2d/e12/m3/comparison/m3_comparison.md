# m3 Comparison

- Notes: Same protocol as E10 (train from scratch on Arduino train, eval Arduino test, train_zscore) but T=50 (2.5 s @ 20 Hz). Compare to E10 (T=100) for window-length apples-to-apples.

| pipeline | protocol | model | accuracy | macro_f1 | model_size_kb | training_time_sec | inference_latency_ms_median | inference_latency_ms_p95 | paper_target_accuracy | acc_delta_vs_target | ptq_status | qat_status | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WISDM replication | random_stratified | baseline float | 0.9886435331230284 | 0.988637669143151 | 80.40625 | 17.908645304999993 | — | — | — | — | ok | ok | ok |
| WISDM replication | random_stratified | PTQ int8 | 0.9889589905362776 | 0.9889540405258309 | 26.1328125 | — | 0.04474099998219572 | 0.05922100000077535 | — | — | ok | — | ok |
| WISDM replication | random_stratified | QAT int8 | 0.98801261829653 | 0.9879831314293082 | 26.734375 | 7.530132320000007 | 0.0464205000128004 | 0.06205850002061197 | — | — | — | ok | ok |
| paper target | — | baseline float | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | PTQ int8 | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | QAT int8 | — | — | — | — | — | — | — | — | — | — | reference |

