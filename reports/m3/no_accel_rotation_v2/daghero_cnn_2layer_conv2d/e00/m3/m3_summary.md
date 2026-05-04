# m3 Summary

- Protocol: `random_stratified`
- Rows: `1`

| paper_slug | protocol | variant | run_mode | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | model_size_kb | paper_target_score | delta_vs_paper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | daghero_cnn_2layer_conv2d | sanity_check | 0.9922446590576529 | 0.9894639736959916 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 41.407536686000014 | 80.40625 | ok | ok | 0.9922446590576529 | 0.9894639736959916 | 15.453625466999995 | 0.07530650000830974 | 0.09158225000760467 | 0.07584650001035698 | 0.0989747500170779 | 26.1328125 | 26.734375 | 26.1328125 | — | — |

