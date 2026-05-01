# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | tcn_attention_har_teacher_conv2d | E12_tcn_attention_har_teacher_conv2d_r0 | sanity_check | ptq_qat_only | 0.9785488958990536 | 0.9785476774451075 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 41.08885654000005 | 1883.1640625 | ok | ok | 0.9785488958990536 | 0.9785476774451075 | 47.36326194200001 | 4.254916999968827 | 4.424997250026763 | 4.2763220000097135 | 4.507730000028687 | 578.3515625 | 585.546875 | — | — | — |

