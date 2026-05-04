# m3 Summary

- Protocol: `random_stratified`
- Rows: `1`

| paper_slug | protocol | variant | run_mode | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | model_size_kb | paper_target_score | delta_vs_paper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | daghero_cnn_2layer_conv2d | sanity_check | 0.16624525916561314 | 0.04751580849141825 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 32.98599294799999 | 80.40625 | ok | ok | 0.16624525916561314 | 0.04751580849141825 | 13.50844091600004 | 0.07509600004595995 | 0.09133674998906827 | 0.07521100002350067 | 0.08372449997295917 | 26.1328125 | 26.734375 | 26.1328125 | — | — |

