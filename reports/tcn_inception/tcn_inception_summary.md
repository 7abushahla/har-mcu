# tcn_inception Summary

- Protocol: `user_holdout`
- Rows: `1`

| paper_slug | protocol | variant | run_mode | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | model_size_kb | paper_target_score | delta_vs_paper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| tcn_inception | user_holdout | tcn_inception_conv2d | sanity_check | 0.8149560117302053 | 0.7430573804582373 | ok | ok | gpu | gpu | gpu | gpu | gpu | gpu | 48.31784683199976 | 1331.265625 | ok | 126.98800381700039 | 3.0616479998570867 | 3.159566250133139 | 3.268084999490384 | 3.333332500005781 | 379.4453125 | 384.8125 | 379.4453125 | — | — |

