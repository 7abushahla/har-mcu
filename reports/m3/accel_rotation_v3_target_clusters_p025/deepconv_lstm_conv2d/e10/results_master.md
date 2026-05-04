# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | deepconv_lstm_conv2d | E10_deepconv_lstm_r0 | sanity_check | ptq_qat_only | 0.9905183312262958 | 0.9905180733831899 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 19.670751495000104 | 513.6171875 | ok | ok | 0.9791403286978508 | 0.9792432680213343 | 7.245232531000056 | 4.256251999890992 | 4.369151499929558 | 4.254078999906596 | 4.344323500106384 | 136.921875 | 137.34375 | — | — | — |

