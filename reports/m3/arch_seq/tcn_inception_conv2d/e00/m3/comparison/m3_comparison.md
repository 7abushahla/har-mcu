# m3 Comparison

- Notes: M3 WISDM M2 anchor.

| pipeline | protocol | model | accuracy | macro_f1 | model_size_kb | training_time_sec | inference_latency_ms_median | inference_latency_ms_p95 | paper_target_accuracy | acc_delta_vs_target | ptq_status | qat_status | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WISDM replication | random_stratified | baseline float | 0.9964881474978051 | 0.9948351650057119 | 1322.98828125 | 141.74638100299998 | — | — | — | — | ok | ok | ok |
| WISDM replication | random_stratified | PTQ int8 | 0.9964881474978051 | 0.9949451241524502 | 369.921875 | — | 2.398085500004754 | 2.424983499992095 | — | — | ok | — | ok |
| WISDM replication | random_stratified | QAT int8 | 0.9976587649985367 | 0.9963603925280419 | 378.375 | 74.162549039 | 2.4819869999532784 | 2.5136670000165395 | — | — | — | ok | ok |
| paper target | — | baseline float | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | PTQ int8 | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | QAT int8 | — | — | — | — | — | — | — | — | — | — | reference |

