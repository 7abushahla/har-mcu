# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | daghero_cnn_2layer_conv2d | E12_daghero_cnn_2layer_conv2d_r0 | sanity_check | ptq_qat_only | 0.983596214511041 | 0.9836004614542538 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 21.183129967000013 | 80.40625 | ok | ok | 0.983596214511041 | 0.9836004614542538 | 8.49198993799996 | 0.0445860000581888 | 0.05153374991095916 | 0.04460050013221917 | 0.05742599995528508 | 26.1328125 | 26.734375 | — | — | — |

