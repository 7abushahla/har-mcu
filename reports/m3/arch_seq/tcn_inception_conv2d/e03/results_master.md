# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | tcn_inception_conv2d | E03_tcn_inception_conv2d_r0 | sanity_check | ptq_qat_only | 0.16624525916561314 | 0.04751580849141825 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 93.26290171800008 | 1322.98828125 | ok | ok | 0.16624525916561314 | 0.04751580849141825 | 73.00050913200005 | 2.400265999938256 | 2.4367094999320216 | 2.4911520000614473 | 2.536568000010675 | 369.921875 | 378.375 | — | — | zero_shot source=wisdm eval=arduino; target arrays normalized with source train stats |

