# M3 Experiment Master

- Total rows: `1`

| experiment_id | model_variant | data_source | train_domain | eval_domain | sample_rate_hz | target_sample_rate_hz | downsample | window_size_samples | window_duration_seconds | overlap | unit_mode | normalization_mode | inference_norm_applied | split_protocol | transfer_mode | seed | fp32_accuracy | fp32_macro_f1 | ptq_accuracy | ptq_macro_f1 | qat_accuracy | qat_macro_f1 | model_size_kb | latency_mean_ms | latency_median_ms | latency_p95_ms | deploy_gate_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E05_legacy_arduino_to_mps2 | deepconv_lstm_conv2d | wisdm_arduino | wisdm | arduino | 20.0 | 20.0 | False | 100 | 5.0 | 0.5 | arduino_to_mps2_legacy | train_zscore | True | random_stratified | zero_shot | 42 | 0.6087231352718079 | 0.6201828907842567 | 0.5809102402022756 | 0.5972976412507511 | 0.5309734513274337 | 0.5426539241965976 | 136.921875 | 4.3087576875013855 | 4.288746500009211 | 4.4268722499936075 | ptq=ok;qat=ok | run_id=E05_deepconv_lstm_r0; fp32_tflite=ok; ptq=ok; qat=ok; zero_shot source=wisdm eval=arduino; target arrays normalized with source train stats; Legacy negative-control Arduino conversion to m/s^2. |
