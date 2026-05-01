# M3 Experiment Master

- Total rows: `1`

| experiment_id | model_variant | data_source | train_domain | eval_domain | sample_rate_hz | target_sample_rate_hz | downsample | window_size_samples | window_duration_seconds | overlap | unit_mode | normalization_mode | inference_norm_applied | split_protocol | transfer_mode | seed | fp32_accuracy | fp32_macro_f1 | ptq_accuracy | ptq_macro_f1 | qat_accuracy | qat_macro_f1 | model_size_kb | latency_mean_ms | latency_median_ms | latency_p95_ms | deploy_gate_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E08_T50_window | tcn_attention_har_teacher_conv2d | wisdm_arduino | wisdm | arduino | 20.0 | 20.0 | False | 50 | 2.5 | 0.5 | raw_no_conversion | train_zscore | True | random_stratified | zero_shot | 42 | 0.1665615141955836 | 0.04759329367225527 | 0.1665615141955836 | 0.04759329367225527 | 0.1665615141955836 | 0.04759329367225527 | 578.3515625 | 4.422338675759363 | 4.421019999881537 | 4.494081999837363 | ptq=ok;qat=ok | run_id=E08_tcn_attention_har_teacher_conv2d_r0; fp32_tflite=ok; ptq=ok; qat=ok; zero_shot source=wisdm eval=arduino; target arrays normalized with source train stats; 20 Hz T50 window-size ablation. |

