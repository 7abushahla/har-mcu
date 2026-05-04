# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | deepconv_lstm_conv2d | E05_deepconv_lstm_r0 | sanity_check | ptq_qat_only | 0.5151706700379267 | 0.4469346095372822 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 69.48457500000006 | 513.6171875 | ok | ok | 0.5202275600505689 | 0.4515050859850376 | 20.757268518999922 | 4.2566380000153 | 4.340256500057649 | 4.2546330000163834 | 4.332784000013135 | 136.921875 | 137.34375 | — | — | zero_shot source=wisdm eval=arduino; target arrays normalized with source train stats |

