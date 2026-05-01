# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | tcn_inception_conv2d | E04_tcn_inception_conv2d_r0 | sanity_check | ptq_qat_only | 0.5018963337547409 | 0.47255669226657987 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 95.84689253099998 | 1322.98828125 | ok | ok | 0.5018963337547409 | 0.47255669226657987 | 74.02692179300004 | 2.402425500008576 | 2.44177425005887 | 2.486059000034402 | 2.517010000076425 | 369.921875 | 378.375 | — | — | zero_shot source=wisdm eval=arduino; target arrays normalized with source train stats |

