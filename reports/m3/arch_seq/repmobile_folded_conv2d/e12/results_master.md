# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | repmobile_folded_conv2d | E12_repmobile_folded_conv2d_r0 | sanity_check | ptq_qat_only | 0.950788643533123 | 0.950782114325163 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 20.457111180000027 | 93.3828125 | ok | ok | 0.950788643533123 | 0.950782114325163 | 13.280862230000025 | 0.17226800000003095 | 0.19241049999152438 | 0.17463199998246637 | 0.19105475000458227 | 42.125 | 43.2578125 | — | — | — |

