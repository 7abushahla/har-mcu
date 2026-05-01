# M3 Experiment Master

- Total rows: `1`

| experiment_id | model_variant | data_source | train_domain | eval_domain | sample_rate_hz | target_sample_rate_hz | downsample | window_size_samples | window_duration_seconds | overlap | unit_mode | normalization_mode | inference_norm_applied | split_protocol | transfer_mode | seed | fp32_accuracy | fp32_macro_f1 | ptq_accuracy | ptq_macro_f1 | qat_accuracy | qat_macro_f1 | model_size_kb | latency_mean_ms | latency_median_ms | latency_p95_ms | deploy_gate_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E09_wisdm_pretrain_arduino_finetune | daghero_cnn_2layer_conv2d | wisdm_arduino | arduino | arduino | 20.0 | 20.0 | False | 100 | 5.0 | 0.5 | raw_no_conversion | train_zscore | True | random_stratified | finetune | 42 | 0.995575221238938 | 0.995581790823015 | 0.995575221238938 | 0.9955782735455708 | 0.995575221238938 | 0.9955794984786192 | 26.1328125 | 0.07689888281481316 | 0.07494450005651743 | 0.09088575001214849 | ptq=ok;qat=ok | run_id=E09_daghero_cnn_2layer_conv2d_r0; fp32_tflite=ok; ptq=ok; qat=ok; finetune pretrain=wisdm target=arduino; final normalization fitted on target train split only; Pretrain on WISDM, fine-tune on Arduino train split, evaluate untouched Arduino test split. |

