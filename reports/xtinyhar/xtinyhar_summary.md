# xtinyhar Summary

- Protocol: `user_holdout`
- Rows: `1`

| paper_slug | protocol | variant | run_mode | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | model_size_kb | paper_target_score | delta_vs_paper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| xtinyhar | user_holdout | xtinyhar_student_conv2d | sanity_check | 0.7686217008797654 | 0.6084267116743621 | failed | failed | gpu | gpu | gpu | gpu | cpu | cpu | 34.648609484996996 | 15.396848472009879 | 0.18489050853531808 | 0.21252024453133345 | 0.18340050155529752 | 0.20328325263108127 | 119.234375 | 119.5859375 | 119.234375 | — | — |

