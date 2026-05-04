# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | deepconv_lstm_conv2d | E08_deepconv_lstm_r0 | sanity_check | ptq_qat_only | 0.1665615141955836 | 0.04759329367225527 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 84.72057308399997 | 396.4296875 | ok | ok | 0.1665615141955836 | 0.04759329367225527 | 35.34705821 | 2.0421340000211785 | 2.0886800000141648 | 2.045363500002395 | 2.0961074999945595 | 107.625 | 108.046875 | — | — | zero_shot source=wisdm eval=arduino; target arrays normalized with source train stats |

