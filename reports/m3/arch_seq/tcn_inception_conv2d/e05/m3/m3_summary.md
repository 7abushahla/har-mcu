# m3 Summary

- Protocol: `random_stratified`
- Rows: `1`

| paper_slug | protocol | variant | run_mode | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | model_size_kb | paper_target_score | delta_vs_paper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | tcn_inception_conv2d | sanity_check | 0.5398230088495575 | 0.4786882462954953 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 119.56388766700002 | 1322.98828125 | ok | ok | 0.5398230088495575 | 0.4786882462954953 | 72.6712073650001 | 2.4136255000257734 | 2.4395452499561543 | 2.513862499995412 | 2.5409329999774855 | 369.921875 | 378.375 | 369.921875 | — | — |

