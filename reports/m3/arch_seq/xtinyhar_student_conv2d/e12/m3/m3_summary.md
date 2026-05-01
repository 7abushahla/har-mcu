# m3 Summary

- Protocol: `random_stratified`
- Rows: `1`

| paper_slug | protocol | variant | run_mode | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | model_size_kb | paper_target_score | delta_vs_paper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | xtinyhar_student_conv2d | sanity_check | 0.9586750788643533 | 0.9585742791206857 | failed | failed | gpu | gpu | gpu | gpu | cpu | cpu | 34.25059137899996 | 1088.77734375 | ok | ok | 0.9586750788643533 | 0.9585742791206857 | 15.798844211000073 | 0.3188599999930375 | 0.33952250001334505 | 0.3199949999839191 | 0.33937500001002263 | 311.4609375 | 311.9296875 | 311.4609375 | — | — |

