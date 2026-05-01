# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | deepconv_lstm_conv2d | E04_deepconv_lstm_r0 | sanity_check | ptq_qat_only | 0.5935524652338812 | 0.6189147088769428 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 49.65904065000001 | 513.6171875 | ok | ok | 0.5644753476611883 | 0.5908057817370408 | 18.249521500000014 | 4.249240999996573 | 4.353442000038399 | 4.253019999993057 | 4.332039000018995 | 136.921875 | 137.34375 | — | — | zero_shot source=wisdm eval=arduino; target arrays normalized with source train stats |
