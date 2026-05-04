# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | daghero_cnn_2layer_conv2d | E08_daghero_cnn_2layer_conv2d_r0 | sanity_check | ptq_qat_only | 0.1665615141955836 | 0.04759329367225527 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 62.29193812699998 | 80.40625 | ok | ok | 0.1665615141955836 | 0.04759329367225527 | 25.21933307300003 | 0.04496100007145287 | 0.06194849999019425 | 0.044855499993445846 | 0.05217825000158882 | 26.1328125 | 26.734375 | — | — | zero_shot source=wisdm eval=arduino; target arrays normalized with source train stats |

