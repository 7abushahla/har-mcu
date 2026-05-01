# m3 Summary

- Protocol: `random_stratified`
- Rows: `1`

| paper_slug | protocol | variant | run_mode | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | model_size_kb | paper_target_score | delta_vs_paper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | xtinyhar_student_conv2d | sanity_check | 0.9791403286978508 | 0.9791259554153061 | failed | failed | gpu | gpu | gpu | gpu | cpu | cpu | 26.057304768999984 | 1103.83203125 | ok | ok | 0.9791403286978508 | 0.9791259554153061 | 10.888250008000114 | 0.32738499999140913 | 0.3579245001219533 | 0.3250765000757383 | 0.356280500000139 | 315.2109375 | 315.6796875 | 315.2109375 | — | — |

