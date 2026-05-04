# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | daghero_cnn_2layer_conv2d | E05_daghero_cnn_2layer_conv2d_r0 | sanity_check | ptq_qat_only | 0.5075853350189633 | 0.4502727934568129 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 38.23599393500001 | 80.40625 | ok | ok | 0.5075853350189633 | 0.4502727934568129 | 15.321436248000055 | 0.07497199999306758 | 0.09150474997454694 | 0.07597199999054283 | 0.09228775004999079 | 26.1328125 | 26.734375 | — | — | zero_shot source=wisdm eval=arduino; target arrays normalized with source train stats |

