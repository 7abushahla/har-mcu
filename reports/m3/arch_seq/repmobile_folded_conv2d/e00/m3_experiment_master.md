# M3 Experiment Master

- Total rows: `1`

| experiment_id | model_variant | data_source | train_domain | eval_domain | sample_rate_hz | target_sample_rate_hz | downsample | window_size_samples | window_duration_seconds | overlap | unit_mode | normalization_mode | inference_norm_applied | split_protocol | transfer_mode | seed | fp32_accuracy | fp32_macro_f1 | ptq_accuracy | ptq_macro_f1 | qat_accuracy | qat_macro_f1 | model_size_kb | latency_mean_ms | latency_median_ms | latency_p95_ms | deploy_gate_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E00_wisdm_m2_anchor | repmobile_folded_conv2d | wisdm | wisdm | wisdm | 20.0 | 20.0 | False | 100 | 5.0 | 0.5 | raw_no_conversion | train_zscore | True | random_stratified | source_only | 42 | 0.9416154521510096 | 0.915202284250101 | 0.9417617793386011 | 0.9147946364819458 | 0.9536142815335089 | 0.9340028169212138 | 42.125 | 0.3319035468756226 | 0.3258505000189871 | 0.354818249974187 | ptq=ok;qat=ok | run_id=E00_repmobile_folded_conv2d_r0; fp32_tflite=ok; ptq=ok; qat=ok; M3 WISDM M2 anchor. |

