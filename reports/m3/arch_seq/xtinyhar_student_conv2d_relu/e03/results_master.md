# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | xtinyhar_student_conv2d_relu | E03_xtinyhar_student_conv2d_relu_r0 | sanity_check | ptq_qat_only | 0.16687737041719342 | 0.04777415852334419 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 61.144084217 | 1101.16015625 | ok | ok | 0.16687737041719342 | 0.04777415852334419 | 28.404267715999993 | 0.3226664999829154 | 0.34729199998650984 | 0.32469149996927626 | 0.34998274998088164 | 312.3671875 | 312.8203125 | — | — | zero_shot source=wisdm eval=arduino; target arrays normalized with source train stats |

