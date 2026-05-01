# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | repmobile_folded_conv2d | E05_repmobile_folded_conv2d_r0 | sanity_check | ptq_qat_only | 0.48419721871049304 | 0.43968655540727514 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 39.44801329699999 | 93.3828125 | ok | ok | 0.48419721871049304 | 0.43968655540727514 | 25.197169459000065 | 0.32636999998203464 | 0.3418274999376081 | 0.32707499997286504 | 0.44361700000195015 | 42.125 | 43.2578125 | — | — | zero_shot source=wisdm eval=arduino; target arrays normalized with source train stats |

