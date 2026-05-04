# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | deepconv_lstm_conv2d | E11_deepconv_lstm_r0 | sanity_check | ptq_qat_only | 0.979179810725552 | 0.9792289331432701 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 12.503588439000168 | 396.4296875 | ok | ok | 0.9444794952681388 | 0.9456433829258946 | 10.18541610300008 | 2.0400864999601254 | 2.0677917500506737 | 2.03774599992812 | 2.0660869999460374 | 107.625 | 108.046875 | — | — | finetune pretrain=wisdm target=arduino; final normalization fitted on target train split only |

