# tcn_attention_har Comparison

- Notes: Teacher WISDM target from paper; PTQ/QAT are replication extensions.

| pipeline | protocol | model | accuracy | macro_f1 | model_size_kb | training_time_sec | inference_latency_ms_median | inference_latency_ms_p95 | paper_target_accuracy | acc_delta_vs_target | ptq_status | qat_status | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WISDM replication | random_stratified | baseline float | 0.9954434993924666 | 0.9903021488633822 | 1923.36328125 | 135.17593838799985 | — | — | 0.9903 | 0.005143499392466611 | failed | failed | ok |
| WISDM replication | random_stratified | PTQ int8 | 0.9948359659781288 | 0.9890033257667884 | 623.9921875 | — | 11.10680500005401 | 11.54039375001048 | — | — | failed | — | failed |
| WISDM replication | random_stratified | QAT int8 | 0.9963547995139733 | 0.9929090180286968 | 631.390625 | 168.62767994900014 | 11.01216650022252 | 11.392862999969111 | — | — | — | failed | failed |
| WISDM replication | user_holdout | baseline float | 0.8609970674486803 | 0.7952953983141998 | 1923.36328125 | 65.12211115399987 | — | — | 0.9903 | -0.12930293255131964 | failed | failed | ok |
| WISDM replication | user_holdout | PTQ int8 | 0.8633431085043989 | 0.7985449346906224 | 623.9921875 | — | 10.646475500152519 | 10.927300500043202 | — | — | failed | — | failed |
| WISDM replication | user_holdout | QAT int8 | 0.8709677419354839 | 0.8169184873380031 | 631.390625 | 165.4217029360002 | 10.738764500047182 | 10.95392224999614 | — | — | — | failed | failed |
| paper target | — | baseline float | 0.9903 | — | — | — | — | — | 0.9903 | — | — | — | reference |
| paper target | — | PTQ int8 | — | — | — | — | — | — | — | — | — | — | reference |
| paper target | — | QAT int8 | — | — | — | — | — | — | — | — | — | — | reference |

