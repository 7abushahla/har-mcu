# M3 Experiment Master

- Total rows: `1`

| experiment_id | model_variant | data_source | train_domain | eval_domain | sample_rate_hz | target_sample_rate_hz | downsample | window_size_samples | window_duration_seconds | overlap | unit_mode | normalization_mode | inference_norm_applied | split_protocol | transfer_mode | seed | fp32_accuracy | fp32_macro_f1 | ptq_accuracy | ptq_macro_f1 | qat_accuracy | qat_macro_f1 | model_size_kb | latency_mean_ms | latency_median_ms | latency_p95_ms | deploy_gate_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E06_no_norm_matched | daghero_cnn_2layer_conv2d | wisdm_arduino | wisdm | arduino | 20.0 | 20.0 | False | 100 | 5.0 | 0.5 | raw_no_conversion | none | False | random_stratified | zero_shot | 42 | 0.16624525916561314 | 0.04751580849141825 | 0.16624525916561314 | 0.04751580849141825 | 0.16624525916561314 | 0.04751580849141825 | 26.1328125 | 0.07753361327633712 | 0.0753245000169045 | 0.09204600004864005 | ptq=ok;qat=ok | run_id=E06_daghero_cnn_2layer_conv2d_r0; fp32_tflite=ok; ptq=ok; qat=ok; zero_shot source=wisdm eval=arduino; target arrays normalized with source train stats; Matched no-normalization training and inference ablation. |

