# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | deepconv_lstm_conv2d | E07_deepconv_lstm_r0 | sanity_check | ptq_qat_only | 0.26169405815423513 | 0.129888500900007 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 57.588537957 | 513.6171875 | ok | ok | 0.29898862199747156 | 0.1517867541088612 | 18.43252721099998 | 4.250723499978903 | 4.279486000015709 | 4.245615999991514 | 4.295132249993117 | 136.921875 | 137.34375 | — | — | zero_shot source=wisdm eval=arduino; target arrays normalized with source train stats |
