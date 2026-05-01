# M3 Experiment Master

- Total rows: `1`

| experiment_id | model_variant | data_source | train_domain | eval_domain | sample_rate_hz | target_sample_rate_hz | downsample | window_size_samples | window_duration_seconds | overlap | unit_mode | normalization_mode | inference_norm_applied | split_protocol | transfer_mode | seed | fp32_accuracy | fp32_macro_f1 | ptq_accuracy | ptq_macro_f1 | qat_accuracy | qat_macro_f1 | model_size_kb | latency_mean_ms | latency_median_ms | latency_p95_ms | deploy_gate_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E04_wisdm_to_g_arduino_g | repmobile_folded_conv2d | wisdm_arduino | wisdm | arduino | 20.0 | 20.0 | False | 100 | 5.0 | 0.5 | wisdm_to_g | train_zscore | True | random_stratified | zero_shot | 42 | 0.48672566371681414 | 0.442449558355321 | 0.4595448798988622 | 0.41376846246063526 | 0.4222503160556258 | 0.3732703955002164 | 42.125 | 0.3286083242179938 | 0.32317500000544896 | 0.3422857500225973 | ptq=ok;qat=ok | run_id=E04_repmobile_folded_conv2d_r0; fp32_tflite=ok; ptq=ok; qat=ok; zero_shot source=wisdm eval=arduino; target arrays normalized with source train stats; Convert WISDM to g and undo Arduino firmware divide-by-four only. |

