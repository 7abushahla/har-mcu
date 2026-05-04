# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | daghero_cnn_2layer_conv2d | E12_daghero_cnn_2layer_conv2d_r0 | sanity_check | ptq_qat_only | 0.9716088328075709 | 0.9714772369415224 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 20.978216153999938 | 80.40625 | ok | ok | 0.9719242902208202 | 0.9717931210334195 | 8.46995103900008 | 0.045266000029187126 | 0.05408349994695527 | 0.04526049997366499 | 0.05139349985938679 | 26.1328125 | 26.734375 | — | — | — |

