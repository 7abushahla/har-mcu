# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | xtinyhar_student_conv2d | E06_xtinyhar_student_conv2d_r0 | sanity_check | ptq_qat_only | 0.17193426042983564 | 0.13033029603312798 | failed | failed | gpu | gpu | gpu | gpu | cpu | cpu | 53.88953816399999 | 1103.77734375 | ok | ok | 0.17193426042983564 | 0.13033029603312798 | 28.276146369000003 | 0.32204400002910916 | 0.3452360000153476 | 0.3229640000768086 | 0.34493500001531174 | 315.2109375 | 315.6796875 | — | — | zero_shot source=wisdm eval=arduino; target arrays normalized with source train stats |

