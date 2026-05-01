# M3 Experiment Master

- Total rows: `1`

| experiment_id | model_variant | data_source | train_domain | eval_domain | sample_rate_hz | target_sample_rate_hz | downsample | window_size_samples | window_duration_seconds | overlap | unit_mode | normalization_mode | inference_norm_applied | split_protocol | transfer_mode | seed | fp32_accuracy | fp32_macro_f1 | ptq_accuracy | ptq_macro_f1 | qat_accuracy | qat_macro_f1 | model_size_kb | latency_mean_ms | latency_median_ms | latency_p95_ms | deploy_gate_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E03_arduino_downsample_20hz_T100 | tcn_inception_conv2d | wisdm_arduino | wisdm | arduino | 20.0 | 20.0 | False | 100 | 5.0 | 0.5 | raw_no_conversion | train_zscore | True | random_stratified | zero_shot | 42 | 0.16624525916561314 | 0.04751580849141825 | 0.16624525916561314 | 0.04751580849141825 | 0.16624525916561314 | 0.04751580849141825 | 369.921875 | 2.403885781254278 | 2.400265999938256 | 2.4367094999320216 | ptq=ok;qat=ok | run_id=E03_tcn_inception_conv2d_r0; fp32_tflite=ok; ptq=ok; qat=ok; zero_shot source=wisdm eval=arduino; target arrays normalized with source train stats; WISDM-compatible Arduino zero-shot using the current 20 Hz merged numeric-user CSV. |

