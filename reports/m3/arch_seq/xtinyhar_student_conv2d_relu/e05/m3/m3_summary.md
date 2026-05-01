# m3 Summary

- Protocol: `random_stratified`
- Rows: `1`

| paper_slug | protocol | variant | run_mode | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | model_size_kb | paper_target_score | delta_vs_paper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | xtinyhar_student_conv2d_relu | sanity_check | 0.5638432364096081 | 0.5882024461291236 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 58.79952724399993 | 1101.16015625 | ok | ok | 0.5638432364096081 | 0.5882024461291236 | 28.031957231999968 | 0.32447699999238466 | 0.34609700000487464 | 0.3256919999898855 | 0.34604525001213915 | 312.3671875 | 312.8203125 | 312.3671875 | — | — |

