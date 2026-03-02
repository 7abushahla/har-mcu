# repmobile Summary

- Protocol: `user_holdout`
- Rows: `1`

| paper_slug | protocol | variant | run_mode | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | model_size_kb | paper_target_score | delta_vs_paper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| repmobile | user_holdout | repmobile_folded_conv2d | sanity_check | 0.7372434017595307 | 0.5323846994461402 | failed | failed | gpu | gpu | gpu | gpu | cpu | cpu | 19.805762067000614 | 39.64139947600779 | 0.40797999827191234 | 0.4412935049913358 | 0.539925997145474 | 0.6573759965249337 | 43.4140625 | 46.9140625 | 43.4140625 | — | — |

