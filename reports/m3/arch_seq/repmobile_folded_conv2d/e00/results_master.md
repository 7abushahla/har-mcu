# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | repmobile_folded_conv2d | E00_repmobile_folded_conv2d_r0 | sanity_check | ptq_qat_only | 0.9416154521510096 | 0.915202284250101 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 42.616925985999984 | 93.3828125 | ok | ok | 0.9416154521510096 | 0.915202284250101 | 25.396587339999996 | 0.3258505000189871 | 0.354818249974187 | 0.32731999999668915 | 0.36691600001859115 | 42.125 | 43.2578125 | — | — | — |

