# M3 Experiment Master

- Total rows: `1`

| experiment_id | model_variant | data_source | train_domain | eval_domain | sample_rate_hz | target_sample_rate_hz | downsample | window_size_samples | window_duration_seconds | overlap | unit_mode | normalization_mode | inference_norm_applied | split_protocol | transfer_mode | seed | fp32_accuracy | fp32_macro_f1 | ptq_accuracy | ptq_macro_f1 | qat_accuracy | qat_macro_f1 | model_size_kb | latency_mean_ms | latency_median_ms | latency_p95_ms | deploy_gate_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E03_arduino_downsample_20hz_T100 | xtinyhar_student_conv2d_relu | wisdm_arduino | wisdm | arduino | 20.0 | 20.0 | False | 100 | 5.0 | 0.5 | raw_no_conversion | train_zscore | True | random_stratified | zero_shot | 42 | 0.16687737041719342 | 0.04777415852334419 | 0.16687737041719342 | 0.04769647696476965 | 0.16687737041719342 | 0.047670639219934995 | 312.3671875 | 0.3277297070312102 | 0.3226664999829154 | 0.34729199998650984 | ptq=ok;qat=ok | run_id=E03_xtinyhar_student_conv2d_relu_r0; fp32_tflite=ok; ptq=ok; qat=ok; zero_shot source=wisdm eval=arduino; target arrays normalized with source train stats; WISDM-compatible Arduino zero-shot using the current 20 Hz merged numeric-user CSV. |

