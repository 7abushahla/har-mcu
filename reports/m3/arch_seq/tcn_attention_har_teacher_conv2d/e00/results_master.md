# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | tcn_attention_har_teacher_conv2d | E00_tcn_attention_har_teacher_conv2d_r0 | sanity_check | ptq_qat_only | 0.9942932396839332 | 0.9915117203094934 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 161.581134272 | 1883.359375 | ok | ok | 0.9942932396839332 | 0.9915117203094934 | 91.73268636599994 | 8.258283499998242 | 8.572420999996666 | 8.317568999984815 | 8.644121749995293 | 578.3984375 | 585.59375 | — | — | — |

