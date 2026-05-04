# m3 Comparison

- Notes: Train from scratch on Arduino train split and evaluate untouched Arduino test split.

| pipeline | protocol | model | accuracy | macro_f1 | model_size_kb | training_time_sec | inference_latency_ms_median | inference_latency_ms_p95 | paper_target_accuracy | acc_delta_vs_target | ptq_status | qat_status | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WISDM replication | random_stratified | baseline float | 0.9905183312262958 | 0.9905180733831899 | 513.6171875 | 19.670751495000104 | — | — | — | — | ok | ok | ok |
| WISDM replication | random_stratified | PTQ int8 | 0.9804045512010113 | 0.9804955200263764 | 136.921875 | — | 4.256251999890992 | 4.369151499929558 | — | — | ok | — | ok |
| WISDM replication | random_stratified | QAT int8 | 0.5335018963337548 | 0.5151757380084843 | 137.34375 | 7.245232531000056 | 4.254078999906596 | 4.344323500106384 | — | — | — | ok | ok |
| paper target | — | baseline float | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | PTQ int8 | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | QAT int8 | — | — | — | — | — | — | — | — | — | — | reference |

