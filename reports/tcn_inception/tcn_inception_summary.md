# tcn_inception Summary

- Protocol: `user_holdout`
- Rows: `1`

| paper_slug | protocol | variant | run_mode | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | model_size_kb | paper_target_score | delta_vs_paper |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| tcn_inception | user_holdout | tcn_inception_conv2d | sanity_check | 0.7656891495601174 | 0.6955700191114071 | failed | failed | gpu | gpu | gpu | gpu | cpu | cpu | 43.186185604994535 | 373.5386522579938 | 3.281900499132462 | 3.8225850112212356 | 3.3888000034494326 | 3.5974382590211462 | 379.4453125 | 384.8125 | 379.4453125 | — | — |

