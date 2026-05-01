# M3 Experiment Master

- Total rows: `1`

| experiment_id | model_variant | data_source | train_domain | eval_domain | sample_rate_hz | target_sample_rate_hz | downsample | window_size_samples | window_duration_seconds | overlap | unit_mode | normalization_mode | inference_norm_applied | split_protocol | transfer_mode | seed | fp32_accuracy | fp32_macro_f1 | ptq_accuracy | ptq_macro_f1 | qat_accuracy | qat_macro_f1 | model_size_kb | latency_mean_ms | latency_median_ms | latency_p95_ms | deploy_gate_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E06_no_norm_matched | tcn_attention_har_teacher_conv2d | wisdm_arduino | wisdm | arduino | 20.0 | 20.0 | False | 100 | 5.0 | 0.5 | raw_no_conversion | none | False | random_stratified | zero_shot | 42 | 0.3501896333754741 | 0.28839272674289523 | 0.4304677623261694 | 0.3940411707564359 | 0.42983565107458915 | 0.37943056206529263 | 578.3984375 | 8.293739375006659 | 8.222651999972186 | 8.645725999940623 | ptq=ok;qat=ok | run_id=E06_tcn_attention_har_teacher_conv2d_r0; fp32_tflite=ok; ptq=ok; qat=ok; zero_shot source=wisdm eval=arduino; target arrays normalized with source train stats; Matched no-normalization training and inference ablation. |

