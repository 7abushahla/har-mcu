# M3 Experiment Master

- Total rows: `1`

| experiment_id | model_variant | data_source | train_domain | eval_domain | sample_rate_hz | target_sample_rate_hz | downsample | window_size_samples | window_duration_seconds | overlap | unit_mode | normalization_mode | inference_norm_applied | split_protocol | transfer_mode | seed | fp32_accuracy | fp32_macro_f1 | ptq_accuracy | ptq_macro_f1 | qat_accuracy | qat_macro_f1 | model_size_kb | latency_mean_ms | latency_median_ms | latency_p95_ms | deploy_gate_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E04_wisdm_to_g_arduino_g | deepconv_lstm_conv2d | wisdm_arduino | wisdm | arduino | 20.0 | 20.0 | False | 100 | 5.0 | 0.5 | wisdm_to_g | train_zscore | True | random_stratified | zero_shot | 42 | 0.5935524652338812 | 0.6189147088769428 | 0.5549936788874842 | 0.5819986064171062 | 0.5284450063211125 | 0.5414513680850193 | 136.921875 | 4.259676273437041 | 4.249240999996573 | 4.353442000038399 | ptq=ok;qat=ok | run_id=E04_deepconv_lstm_r0; fp32_tflite=ok; ptq=ok; qat=ok; zero_shot source=wisdm eval=arduino; target arrays normalized with source train stats; Convert WISDM to g and undo Arduino firmware divide-by-four only. |
