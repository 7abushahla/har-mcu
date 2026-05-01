# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | xtinyhar_student_conv2d_relu | E11_xtinyhar_student_conv2d_relu_r0 | sanity_check | ptq_qat_only | 0.9555205047318612 | 0.9556081010608821 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 20.41641401700008 | 1086.20703125 | ok | ok | 0.9555205047318612 | 0.9556081010608821 | 15.781715903000077 | 0.3210819999139858 | 0.33638974991845316 | 0.3221015000463012 | 0.3413320000618114 | 308.6171875 | 309.0703125 | — | — | finetune pretrain=wisdm target=arduino; final normalization fitted on target train split only |

