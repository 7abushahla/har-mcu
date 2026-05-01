# M3 Experiment Master

- Total rows: `1`

| experiment_id | model_variant | data_source | train_domain | eval_domain | sample_rate_hz | target_sample_rate_hz | downsample | window_size_samples | window_duration_seconds | overlap | unit_mode | normalization_mode | inference_norm_applied | split_protocol | transfer_mode | seed | fp32_accuracy | fp32_macro_f1 | ptq_accuracy | ptq_macro_f1 | qat_accuracy | qat_macro_f1 | model_size_kb | latency_mean_ms | latency_median_ms | latency_p95_ms | deploy_gate_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E00_wisdm_m2_anchor | xtinyhar_student_conv2d | wisdm | wisdm | wisdm | 20.0 | 20.0 | False | 100 | 5.0 | 0.5 | raw_no_conversion | train_zscore | True | random_stratified | source_only | 42 | 0.9569798068481123 | 0.9442987986633135 | 0.9562481709101551 | 0.9435157979013424 | 0.9615159496634474 | 0.9493589080627994 | 315.2109375 | 0.32652763281082464 | 0.32084450000979814 | 0.3415525000178832 | ptq=failed;qat=failed | run_id=E00_xtinyhar_student_conv2d_r0; fp32_tflite=ok; ptq=failed; qat=failed; M3 WISDM M2 anchor. |

