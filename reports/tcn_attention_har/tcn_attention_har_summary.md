# tcn_attention_har Summary

- Protocol: `user_holdout`
- Rows: `1`

| paper_slug | protocol | variant | run_mode | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | model_size_kb | paper_target_score | delta_vs_paper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| tcn_attention_har | user_holdout | tcn_attention_har_teacher_conv2d | sanity_check | 0.8609970674486803 | 0.7952953983141998 | failed | failed | gpu | gpu | gpu | gpu | gpu | gpu | 65.12211115399987 | 1923.36328125 | ok | 165.4217029360002 | 10.646475500152519 | 10.927300500043202 | 10.738764500047182 | 10.95392224999614 | 623.9921875 | 631.390625 | 623.9921875 | 0.9903 | -0.12930293255131964 |

