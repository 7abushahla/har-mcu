# M3 Experiment Master

- Total rows: `1`

| experiment_id | model_variant | data_source | train_domain | eval_domain | sample_rate_hz | target_sample_rate_hz | downsample | window_size_samples | window_duration_seconds | overlap | unit_mode | normalization_mode | inference_norm_applied | split_protocol | transfer_mode | seed | fp32_accuracy | fp32_macro_f1 | ptq_accuracy | ptq_macro_f1 | qat_accuracy | qat_macro_f1 | model_size_kb | latency_mean_ms | latency_median_ms | latency_p95_ms | deploy_gate_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E00_wisdm_m2_anchor | deepconv_lstm_conv2d | wisdm | wisdm | wisdm | 20.0 | 20.0 | False | 100 | 5.0 | 0.5 | raw_no_conversion | train_zscore | True | random_stratified | source_only | 42 | 0.9884401521802751 | 0.9831177999390307 | 0.9800995024875622 | 0.9713485385927911 | 0.8238220661398888 | 0.7751120983264624 | 136.921875 | 4.26394736328195 | 4.251617999983637 | 4.33369924999738 | ptq=ok;qat=ok | run_id=E00_deepconv_lstm_r0; fp32_tflite=ok; ptq=ok; qat=ok; M3 WISDM M2 anchor. |

