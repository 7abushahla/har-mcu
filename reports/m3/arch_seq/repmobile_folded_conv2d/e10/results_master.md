# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | repmobile_folded_conv2d | E10_repmobile_folded_conv2d_r0 | sanity_check | ptq_qat_only | 0.9627054361567636 | 0.9624606996642625 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 12.556897537000168 | 93.3828125 | ok | ok | 0.9627054361567636 | 0.9624606996642625 | 8.57874334500002 | 0.3239300000359435 | 0.4198192499984543 | 0.32659549992786197 | 0.3434802500805745 | 42.125 | 43.2578125 | — | — | — |

