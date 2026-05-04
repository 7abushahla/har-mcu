# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | deepconv_lstm_conv2d | E10_deepconv_lstm_r0 | sanity_check | ptq_qat_only | 0.9810366624525917 | 0.9809982236312752 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 13.097278664000214 | 513.6171875 | ok | ok | 0.9405815423514539 | 0.9404755169294939 | 6.716068211999982 | 4.243390000169711 | 4.289840750004714 | 4.242439499989814 | 4.2769199999384 | 136.921875 | 137.34375 | — | — | — |

