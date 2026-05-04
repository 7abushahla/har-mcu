# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | deepconv_lstm_conv2d | E12_deepconv_lstm_r0 | sanity_check | ptq_qat_only | 0.9832807570977918 | 0.9833063333917463 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 17.826211867999973 | 396.4296875 | ok | ok | 0.88801261829653 | 0.8930146677342585 | 9.242430423000087 | 2.03662000001259 | 2.062395749874213 | 2.040684999997211 | 2.069550249927943 | 107.625 | 108.046875 | — | — | — |

