# daghero_qadnn Summary

- Protocol: `user_holdout`
- Rows: `1`

| paper_slug | protocol | variant | run_mode | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | model_size_kb | paper_target_score | delta_vs_paper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| daghero_qadnn | user_holdout | daghero_cnn_2layer_conv2d | sanity_check | 0.83841642228739 | 0.8040049281824485 | failed | failed | gpu | gpu | gpu | gpu | cpu | cpu | 11.901672872001654 | 18.77276402899588 | 0.09138500900007784 | 0.10628000018186867 | 0.11734999134205282 | 0.13964250683784485 | 27.3671875 | 29.4140625 | 27.3671875 | — | — |

