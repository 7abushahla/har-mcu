# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | repmobile_folded_conv2d | E09_repmobile_folded_conv2d_r0 | sanity_check | ptq_qat_only | 0.9791403286978508 | 0.9791571324321376 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 10.80227839600002 | 93.3828125 | ok | ok | 0.9791403286978508 | 0.9791571324321376 | 8.623582308000096 | 0.3280549998407878 | 0.34520099990231756 | 0.3239249999751337 | 0.3654485001334251 | 42.125 | 43.2578125 | — | — | finetune pretrain=wisdm target=arduino; final normalization fitted on target train split only |

