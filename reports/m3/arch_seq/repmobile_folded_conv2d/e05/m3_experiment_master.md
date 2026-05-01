# M3 Experiment Master

- Total rows: `1`

| experiment_id | model_variant | data_source | train_domain | eval_domain | sample_rate_hz | target_sample_rate_hz | downsample | window_size_samples | window_duration_seconds | overlap | unit_mode | normalization_mode | inference_norm_applied | split_protocol | transfer_mode | seed | fp32_accuracy | fp32_macro_f1 | ptq_accuracy | ptq_macro_f1 | qat_accuracy | qat_macro_f1 | model_size_kb | latency_mean_ms | latency_median_ms | latency_p95_ms | deploy_gate_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E05_legacy_arduino_to_mps2 | repmobile_folded_conv2d | wisdm_arduino | wisdm | arduino | 20.0 | 20.0 | False | 100 | 5.0 | 0.5 | arduino_to_mps2_legacy | train_zscore | True | random_stratified | zero_shot | 42 | 0.48419721871049304 | 0.43968655540727514 | 0.4633375474083439 | 0.4180572326438093 | 0.4254108723135272 | 0.37674398252250146 | 42.125 | 0.3286138281248796 | 0.32636999998203464 | 0.3418274999376081 | ptq=ok;qat=ok | run_id=E05_repmobile_folded_conv2d_r0; fp32_tflite=ok; ptq=ok; qat=ok; zero_shot source=wisdm eval=arduino; target arrays normalized with source train stats; Legacy negative-control Arduino conversion to m/s^2. |

