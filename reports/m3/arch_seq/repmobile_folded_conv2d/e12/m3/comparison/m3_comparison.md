# m3 Comparison

- Notes: Same protocol as E10 (train from scratch on Arduino train, eval Arduino test, train_zscore) but T=50 (2.5 s @ 20 Hz). Compare to E10 (T=100) for window-length apples-to-apples.

| pipeline | protocol | model | accuracy | macro_f1 | model_size_kb | training_time_sec | inference_latency_ms_median | inference_latency_ms_p95 | paper_target_accuracy | acc_delta_vs_target | ptq_status | qat_status | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WISDM replication | random_stratified | baseline float | 0.950788643533123 | 0.950782114325163 | 93.3828125 | 20.457111180000027 | — | — | — | — | ok | ok | ok |
| WISDM replication | random_stratified | PTQ int8 | 0.9488958990536278 | 0.9488711269454039 | 42.125 | — | 0.17226800000003095 | 0.19241049999152438 | — | — | ok | — | ok |
| WISDM replication | random_stratified | QAT int8 | 0.9580441640378549 | 0.9580247791057515 | 43.2578125 | 13.280862230000025 | 0.17463199998246637 | 0.19105475000458227 | — | — | — | ok | ok |
| paper target | — | baseline float | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | PTQ int8 | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | QAT int8 | — | — | — | — | — | — | — | — | — | — | reference |

