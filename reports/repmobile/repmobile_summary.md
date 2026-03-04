# repmobile Summary

- Protocol: `user_holdout`
- Rows: `1`

| paper_slug | protocol | variant | run_mode | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | model_size_kb | paper_target_score | delta_vs_paper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| repmobile | user_holdout | repmobile_folded_conv2d | sanity_check | 0.7372434017595307 | 0.5323846994461402 | ok | ok | gpu | gpu | gpu | gpu | gpu | gpu | 17.628862212999593 | 94.68359375 | ok | 18.730120572999567 | 0.41620100023465056 | 0.465745749920643 | 0.5446200000278623 | 0.5960000000868604 | 43.4140625 | 46.9140625 | 43.4140625 | — | — |

