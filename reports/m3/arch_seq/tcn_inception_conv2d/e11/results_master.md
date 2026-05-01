# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | tcn_inception_conv2d | E11_tcn_inception_conv2d_r0 | sanity_check | ptq_qat_only | 0.9807570977917981 | 0.9807448213375927 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 33.04100448600002 | 1322.98828125 | ok | ok | 0.9807570977917981 | 0.9807448213375927 | 38.998502547000044 | 1.2858270000606353 | 1.3088702499999272 | 1.4116994999540111 | 1.4385224999386992 | 369.921875 | 378.375 | — | — | finetune pretrain=wisdm target=arduino; final normalization fitted on target train split only |

