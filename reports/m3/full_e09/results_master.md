# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | deepconv_lstm_conv2d | E09_deepconv_lstm_r0 | sanity_check | ptq_qat_only | 0.995575221238938 | 0.9955735520260941 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 14.732664849000003 | 513.6171875 | ok | ok | 0.9911504424778761 | 0.9911600682512675 | 6.612743181000042 | 4.235478499992951 | 4.266791500000977 | 4.241438500002914 | 4.3129124999978785 | 136.921875 | 137.34375 | — | — | finetune pretrain=wisdm target=arduino; final normalization fitted on target train split only |
