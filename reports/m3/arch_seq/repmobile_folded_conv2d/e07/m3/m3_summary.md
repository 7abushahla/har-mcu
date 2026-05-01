# m3 Summary

- Protocol: `random_stratified`
- Rows: `1`

| paper_slug | protocol | variant | run_mode | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | model_size_kb | paper_target_score | delta_vs_paper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | repmobile_folded_conv2d | sanity_check | 0.16687737041719342 | 0.047670639219934995 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 39.54084253499991 | 93.3828125 | ok | ok | 0.16687737041719342 | 0.047670639219934995 | 25.268616758999997 | 0.32711050005218567 | 0.41062450003437334 | 0.32796049998751187 | 0.3681010000207152 | 42.125 | 43.2578125 | 42.125 | — | — |

