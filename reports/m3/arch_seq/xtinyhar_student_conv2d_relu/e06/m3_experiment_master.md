# M3 Experiment Master

- Total rows: `1`

| experiment_id | model_variant | data_source | train_domain | eval_domain | sample_rate_hz | target_sample_rate_hz | downsample | window_size_samples | window_duration_seconds | overlap | unit_mode | normalization_mode | inference_norm_applied | split_protocol | transfer_mode | seed | fp32_accuracy | fp32_macro_f1 | ptq_accuracy | ptq_macro_f1 | qat_accuracy | qat_macro_f1 | model_size_kb | latency_mean_ms | latency_median_ms | latency_p95_ms | deploy_gate_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E06_no_norm_matched | xtinyhar_student_conv2d_relu | wisdm_arduino | wisdm | arduino | 20.0 | 20.0 | False | 100 | 5.0 | 0.5 | raw_no_conversion | none | False | random_stratified | zero_shot | 42 | 0.20480404551201012 | 0.18326356811003688 | 0.12831858407079647 | 0.13402828956543789 | 0.1611883691529709 | 0.06741298612066003 | 312.3671875 | 0.32460806249989815 | 0.320341500014365 | 0.3438620000508763 | ptq=ok;qat=ok | run_id=E06_xtinyhar_student_conv2d_relu_r0; fp32_tflite=ok; ptq=ok; qat=ok; zero_shot source=wisdm eval=arduino; target arrays normalized with source train stats; Matched no-normalization training and inference ablation. |

