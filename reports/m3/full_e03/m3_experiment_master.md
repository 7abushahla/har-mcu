# M3 Experiment Master

- Total rows: `1`

| experiment_id | model_variant | data_source | train_domain | eval_domain | sample_rate_hz | target_sample_rate_hz | downsample | window_size_samples | window_duration_seconds | overlap | unit_mode | normalization_mode | inference_norm_applied | split_protocol | transfer_mode | seed | fp32_accuracy | fp32_macro_f1 | ptq_accuracy | ptq_macro_f1 | qat_accuracy | qat_macro_f1 | model_size_kb | latency_mean_ms | latency_median_ms | latency_p95_ms | deploy_gate_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E03_arduino_downsample_20hz_T100 | deepconv_lstm_conv2d | wisdm_arduino | wisdm | arduino | 20.0 | 20.0 | False | 100 | 5.0 | 0.5 | raw_no_conversion | train_zscore | True | random_stratified | zero_shot | 42 | 0.16624525916561314 | 0.057149065623641894 | 0.18078381795195955 | 0.07033648735776395 | 0.16687737041719342 | 0.047670639219934995 | 136.921875 | 4.258364835934891 | 4.248632999974689 | 4.322087000019792 | ptq=ok;qat=ok | run_id=E03_deepconv_lstm_r0; fp32_tflite=ok; ptq=ok; qat=ok; zero_shot source=wisdm eval=arduino; target arrays normalized with source train stats; WISDM-compatible Arduino zero-shot using the current 20 Hz merged numeric-user CSV. |
