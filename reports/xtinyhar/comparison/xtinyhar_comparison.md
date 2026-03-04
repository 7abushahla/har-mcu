# xtinyhar Comparison

- Notes: Paper reports UTD-MHAD/MM-Fit accuracy; no direct WISDM target.

| pipeline | protocol | model | accuracy | macro_f1 | model_size_kb | training_time_sec | inference_latency_ms_median | inference_latency_ms_p95 | paper_target_accuracy | acc_delta_vs_target | ptq_status | qat_status | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WISDM replication | random_stratified | baseline float | 0.9188942891859052 | 0.8748371963957752 | 320.5390625 | 52.20173649299977 | — | — | — | — | failed | failed | ok |
| WISDM replication | random_stratified | PTQ int8 | 0.9185905224787363 | 0.8741101749999727 | 119.1484375 | — | 0.17823799953475827 | 0.27427274972069426 | — | — | failed | — | failed |
| WISDM replication | random_stratified | QAT int8 | 0.9365127582017011 | 0.908275252200763 | 119.5859375 | 26.643862249999984 | 0.17706849985188455 | 0.2098507497976243 | — | — | — | failed | failed |
| WISDM replication | user_holdout | baseline float | 0.7686217008797654 | 0.6084267116743621 | 320.84375 | 35.25273950200062 | — | — | — | — | failed | failed | ok |
| WISDM replication | user_holdout | PTQ int8 | 0.7700879765395895 | 0.611842800307793 | 119.234375 | — | 0.18373800003246288 | 0.29139275034140155 | — | — | failed | — | failed |
| WISDM replication | user_holdout | QAT int8 | 0.7656891495601174 | 0.6525526800191249 | 119.5859375 | 27.204162859000462 | 0.17666350049694302 | 0.21942775038041873 | — | — | — | failed | failed |
| paper target | — | baseline float | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | PTQ int8 | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | QAT int8 | — | — | — | — | — | — | — | — | — | — | reference |

