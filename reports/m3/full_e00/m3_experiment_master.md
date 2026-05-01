# M3 Experiment Master

- Total rows: `1`

| experiment_id | model_variant | data_source | train_domain | eval_domain | sample_rate_hz | target_sample_rate_hz | downsample | window_size_samples | window_duration_seconds | overlap | unit_mode | normalization_mode | inference_norm_applied | split_protocol | transfer_mode | seed | fp32_accuracy | fp32_macro_f1 | ptq_accuracy | ptq_macro_f1 | qat_accuracy | qat_macro_f1 | model_size_kb | latency_mean_ms | latency_median_ms | latency_p95_ms | deploy_gate_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E00_wisdm_m2_anchor | deepconv_lstm_conv2d | wisdm | wisdm | wisdm | 20.0 | 20.0 | False | 100 | 5.0 | 0.5 | raw_no_conversion | train_zscore | True | random_stratified | source_only | 42 | 0.9885864793678666 | 0.9832806154804284 | 0.9802458296751536 | 0.9719087901072831 | 0.8187006145741879 | 0.7736428461876698 | 136.921875 | 4.256022730468434 | 4.245099499996741 | 4.324175749999881 | ptq=ok;qat=ok | run_id=E00_deepconv_lstm_r0; fp32_tflite=ok; ptq=ok; qat=ok; M3 WISDM M2 anchor. |
