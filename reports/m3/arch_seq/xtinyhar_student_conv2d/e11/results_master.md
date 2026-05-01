# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | xtinyhar_student_conv2d | E11_xtinyhar_student_conv2d_r0 | sanity_check | ptq_qat_only | 0.9615141955835962 | 0.9614971460097643 | failed | failed | gpu | gpu | gpu | gpu | cpu | cpu | 24.567764921999924 | 1088.83203125 | ok | ok | 0.9615141955835962 | 0.9614971460097643 | 16.282887517000063 | 0.33012200003668113 | 0.3657347498915442 | 0.3229210001336469 | 0.33655700008239364 | 311.4609375 | 311.9296875 | — | — | finetune pretrain=wisdm target=arduino; final normalization fitted on target train split only |

