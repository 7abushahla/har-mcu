# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | deepconv_lstm_conv2d | E12_deepconv_lstm_r0 | sanity_check | ptq_qat_only | 0.9845425867507887 | 0.9845330049257986 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 22.438512761999846 | 396.4296875 | ok | ok | 0.9141955835962146 | 0.9170292161924242 | 10.255917209000017 | 2.0391469998912726 | 2.0660195000914428 | 2.037100999928043 | 2.0542534999776763 | 107.625 | 108.046875 | — | — | — |

