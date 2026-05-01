# m3 Summary

- Protocol: `random_stratified`
- Rows: `1`

| paper_slug | protocol | variant | run_mode | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | model_size_kb | paper_target_score | delta_vs_paper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | tcn_attention_har_teacher_conv2d | sanity_check | 0.1665615141955836 | 0.04759329367225527 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 268.61984757300024 | 1883.1640625 | ok | ok | 0.1665615141955836 | 0.04759329367225527 | 173.13161414500019 | 4.421019999881537 | 4.494081999837363 | 4.460026499828018 | 4.582361500069965 | 578.3515625 | 585.546875 | 578.3515625 | — | — |

