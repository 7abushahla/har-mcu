# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | xtinyhar_student_conv2d | E03_xtinyhar_student_conv2d_r0 | sanity_check | ptq_qat_only | 0.16687737041719342 | 0.047670639219934995 | failed | failed | gpu | gpu | gpu | gpu | cpu | cpu | 54.106888443 | 1103.77734375 | ok | ok | 0.16687737041719342 | 0.047670639219934995 | 28.563432057 | 0.32250949999479417 | 0.3442807499709488 | 0.3217395000376655 | 0.3482335000057901 | 315.2109375 | 315.6796875 | — | — | zero_shot source=wisdm eval=arduino; target arrays normalized with source train stats |

