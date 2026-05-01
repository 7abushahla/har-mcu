# M3 Experiment Master

- Total rows: `1`

| experiment_id | model_variant | data_source | train_domain | eval_domain | sample_rate_hz | target_sample_rate_hz | downsample | window_size_samples | window_duration_seconds | overlap | unit_mode | normalization_mode | inference_norm_applied | split_protocol | transfer_mode | seed | fp32_accuracy | fp32_macro_f1 | ptq_accuracy | ptq_macro_f1 | qat_accuracy | qat_macro_f1 | model_size_kb | latency_mean_ms | latency_median_ms | latency_p95_ms | deploy_gate_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E00_wisdm_m2_anchor | xtinyhar_student_conv2d_relu | wisdm | wisdm | wisdm | 20.0 | 20.0 | False | 100 | 5.0 | 0.5 | raw_no_conversion | train_zscore | True | random_stratified | source_only | 42 | 0.9364940005853087 | 0.9139169403752114 | 0.9362013462101259 | 0.9133031459235842 | 0.9511267193444543 | 0.9345297945275495 | 312.3671875 | 0.33727480468837 | 0.3231765000464293 | 0.34764025001265964 | ptq=ok;qat=ok | run_id=E00_xtinyhar_student_conv2d_relu_r0; fp32_tflite=ok; ptq=ok; qat=ok; M3 WISDM M2 anchor. |

