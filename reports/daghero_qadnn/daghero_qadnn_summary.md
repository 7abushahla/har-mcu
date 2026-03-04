# daghero_qadnn Summary

- Protocol: `user_holdout`
- Rows: `1`

| paper_slug | protocol | variant | run_mode | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | model_size_kb | paper_target_score | delta_vs_paper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| daghero_qadnn | user_holdout | daghero_cnn_2layer_conv2d | sanity_check | 0.8208211143695014 | 0.7648593735898475 | ok | ok | gpu | gpu | gpu | gpu | gpu | gpu | 14.96201608499996 | 81.63671875 | ok | 34.82446578600002 | 0.09025449992350332 | 0.10305900002549606 | 0.11503400003221032 | 0.12756124988300144 | 27.3671875 | 29.4140625 | 27.3671875 | — | — |

