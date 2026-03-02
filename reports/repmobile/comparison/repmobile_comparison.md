# repmobile Comparison

- Notes: Paper emphasizes latency and efficiency; WISDM adaptation target accuracy not fixed here.

| pipeline | protocol | model | accuracy | macro_f1 | model_size_kb | training_time_sec | inference_latency_ms_median | inference_latency_ms_p95 | paper_target_accuracy | acc_delta_vs_target | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WISDM replication | random_stratified | baseline float | 0.7715674362089915 | 0.577059167353506 | — | 23.348663579992717 | — | — | — | — | ok |
| WISDM replication | random_stratified | PTQ int8 | 0.7688335358444714 | 0.5744271191201293 | 43.4140625 | — | 0.4046955000376329 | 0.4454810004972387 | — | — | failed |
| WISDM replication | random_stratified | QAT int8 | 0.8071081409477521 | 0.6031907060929053 | 46.9140625 | 43.36158431900549 | 0.5415110063040629 | 0.6000085049890913 | — | — | failed |
| WISDM replication | user_holdout | baseline float | 0.7372434017595307 | 0.5323846994461402 | — | 19.805762067000614 | — | — | — | — | ok |
| WISDM replication | user_holdout | PTQ int8 | 0.7284457478005865 | 0.5315173051412764 | 43.4140625 | — | 0.40797999827191234 | 0.4412935049913358 | — | — | failed |
| WISDM replication | user_holdout | QAT int8 | 0.7627565982404693 | 0.5184094806975891 | 46.9140625 | 39.64139947600779 | 0.539925997145474 | 0.6573759965249337 | — | — | failed |
| paper target | — | baseline float | — | — | — | — | — | — | — | — | reference |
| paper target | — | PTQ int8 | — | — | — | — | — | — | — | — | reference |
| paper target | — | QAT int8 | — | — | — | — | — | — | — | — | reference |

