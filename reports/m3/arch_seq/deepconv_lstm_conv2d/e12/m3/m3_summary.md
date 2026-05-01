# m3 Summary

- Protocol: `random_stratified`
- Rows: `1`

| paper_slug | protocol | variant | run_mode | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | model_size_kb | paper_target_score | delta_vs_paper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | deepconv_lstm_conv2d | sanity_check | 0.9813880126182966 | 0.9814210220702986 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 19.89185975199996 | 396.4296875 | ok | ok | 0.8823343848580442 | 0.8879037273504108 | 9.083264248999967 | 2.0360940000045957 | 2.0707550000338415 | 2.0376644999942073 | 2.068092499982299 | 107.625 | 108.046875 | 107.625 | — | — |

