# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | deepconv_lstm_conv2d | E08_deepconv_lstm_r0 | sanity_check | ptq_qat_only | 0.1668769716088328 | 0.04767054158781653 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 62.33975248900015 | 396.4296875 | ok | ok | 0.1668769716088328 | 0.04767054158781653 | 29.79271824800003 | 2.0426199999974415 | 2.10186425010761 | 2.0452554999792483 | 2.0925265000073523 | 107.625 | 108.046875 | — | — | zero_shot source=wisdm eval=arduino; target arrays normalized with source train stats |

