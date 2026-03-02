# tcn_attention_har Summary

- Protocol: `user_holdout`
- Rows: `1`

| paper_slug | protocol | variant | run_mode | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | model_size_kb | paper_target_score | delta_vs_paper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| tcn_attention_har | user_holdout | tcn_attention_har_teacher_conv2d | sanity_check | 0.8607038123167156 | 0.7936474808556794 | failed | failed | gpu | gpu | gpu | gpu | cpu | cpu | 66.46890478201385 | 514.8198633919965 | 11.328067492286209 | 11.871703740325756 | 11.950079497182742 | 12.350502496701665 | 623.9921875 | 631.390625 | 623.9921875 | 0.9903 | -0.1295961876832844 |

