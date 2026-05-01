# m3 Summary

- Protocol: `random_stratified`
- Rows: `1`

| paper_slug | protocol | variant | run_mode | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | model_size_kb | paper_target_score | delta_vs_paper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | tcn_attention_har_teacher_conv2d | sanity_check | 0.9949431099873578 | 0.9949373834776645 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 27.966597232999902 | 1883.359375 | ok | ok | 0.9949431099873578 | 0.9949373834776645 | 29.121981616000085 | 8.268247000160045 | 8.631353500277328 | 8.169350000116538 | 8.574291750278462 | 578.3984375 | 585.59375 | 578.3984375 | — | — |

