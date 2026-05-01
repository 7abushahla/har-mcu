# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | xtinyhar_student_conv2d_relu | E09_xtinyhar_student_conv2d_relu_r0 | sanity_check | ptq_qat_only | 0.972819216182048 | 0.9727692170310229 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 16.493753922999986 | 1101.20703125 | ok | ok | 0.972819216182048 | 0.9727692170310229 | 10.593193881999923 | 0.32543199995416217 | 0.3485995001142328 | 0.3263070000230073 | 0.35620275002656854 | 312.3671875 | 312.8203125 | — | — | finetune pretrain=wisdm target=arduino; final normalization fitted on target train split only |

