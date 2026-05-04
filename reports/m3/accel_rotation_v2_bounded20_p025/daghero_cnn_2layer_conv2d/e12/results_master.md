# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | daghero_cnn_2layer_conv2d | E12_daghero_cnn_2layer_conv2d_r0 | sanity_check | ptq_qat_only | 0.9864353312302839 | 0.9864129888330441 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 21.213813071000004 | 80.40625 | ok | ok | 0.9864353312302839 | 0.9864129888330441 | 8.397821307999948 | 0.044776000038382335 | 0.04989099997487756 | 0.04525099996044446 | 0.05614849996504745 | 26.1328125 | 26.734375 | — | — | — |

