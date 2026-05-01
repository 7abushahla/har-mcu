# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | deepconv_lstm_conv2d | E06_deepconv_lstm_r0 | sanity_check | ptq_qat_only | 0.16940581542351454 | 0.05495834189992266 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 47.17007765699998 | 513.6171875 | ok | ok | 0.1675094816687737 | 0.051488045841440684 | 18.40579241100005 | 4.270242500012955 | 4.384683499978337 | 4.256062000024485 | 4.368070000012381 | 136.921875 | 137.34375 | — | — | zero_shot source=wisdm eval=arduino; target arrays normalized with source train stats |
