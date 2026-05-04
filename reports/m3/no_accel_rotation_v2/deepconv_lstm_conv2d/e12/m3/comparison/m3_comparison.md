# m3 Comparison

- Notes: Same protocol as E10 (train from scratch on Arduino train, eval Arduino test, train_zscore) but T=50 (2.5 s @ 20 Hz). Compare to E10 (T=100) for window-length apples-to-apples.

| pipeline | protocol | model | accuracy | macro_f1 | model_size_kb | training_time_sec | inference_latency_ms_median | inference_latency_ms_p95 | paper_target_accuracy | acc_delta_vs_target | ptq_status | qat_status | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WISDM replication | random_stratified | baseline float | 0.9832807570977918 | 0.9833063333917463 | 396.4296875 | 17.826211867999973 | — | — | — | — | ok | ok | ok |
| WISDM replication | random_stratified | PTQ int8 | 0.8867507886435331 | 0.8918682532768347 | 107.625 | — | 2.03662000001259 | 2.062395749874213 | — | — | ok | — | ok |
| WISDM replication | random_stratified | QAT int8 | 0.8498422712933754 | 0.8559377991945447 | 108.046875 | 9.242430423000087 | 2.040684999997211 | 2.069550249927943 | — | — | — | ok | ok |
| paper target | — | baseline float | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | PTQ int8 | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | QAT int8 | — | — | — | — | — | — | — | — | — | — | reference |

