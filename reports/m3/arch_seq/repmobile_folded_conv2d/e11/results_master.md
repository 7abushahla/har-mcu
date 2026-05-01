# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | repmobile_folded_conv2d | E11_repmobile_folded_conv2d_r0 | sanity_check | ptq_qat_only | 0.9675078864353313 | 0.967438784185834 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 19.549526361000062 | 93.3828125 | ok | ok | 0.9675078864353313 | 0.967438784185834 | 13.235464621999995 | 0.17082900001241796 | 0.20008900003176677 | 0.1821285000005446 | 0.20438999996486018 | 42.125 | 43.2578125 | — | — | finetune pretrain=wisdm target=arduino; final normalization fitted on target train split only |

