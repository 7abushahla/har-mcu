# m3 Summary

- Protocol: `random_stratified`
- Rows: `1`

| paper_slug | protocol | variant | run_mode | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | model_size_kb | paper_target_score | delta_vs_paper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | xtinyhar_student_conv2d_relu | sanity_check | 0.16687737041719342 | 0.047670639219934995 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 57.75097041699996 | 1101.16015625 | ok | ok | 0.16687737041719342 | 0.047670639219934995 | 28.34414666200007 | 0.32334700000546945 | 0.35193200000094294 | 0.3262870000071416 | 0.34800699995685136 | 312.3671875 | 312.8203125 | 312.3671875 | — | — |

