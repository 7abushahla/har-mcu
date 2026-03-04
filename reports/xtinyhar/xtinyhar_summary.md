# xtinyhar Summary

- Protocol: `user_holdout`
- Rows: `1`

| paper_slug | protocol | variant | run_mode | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | model_size_kb | paper_target_score | delta_vs_paper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| xtinyhar | user_holdout | xtinyhar_student_conv2d | sanity_check | 0.7686217008797654 | 0.6084267116743621 | failed | failed | gpu | gpu | gpu | gpu | gpu | gpu | 35.25273950200062 | 320.84375 | ok | 27.204162859000462 | 0.18373800003246288 | 0.29139275034140155 | 0.17666350049694302 | 0.21942775038041873 | 119.234375 | 119.5859375 | 119.234375 | — | — |

