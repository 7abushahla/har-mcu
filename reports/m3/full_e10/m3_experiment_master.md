# M3 Experiment Master

- Total rows: `1`

| experiment_id | model_variant | data_source | train_domain | eval_domain | sample_rate_hz | target_sample_rate_hz | downsample | window_size_samples | window_duration_seconds | overlap | unit_mode | normalization_mode | inference_norm_applied | split_protocol | transfer_mode | seed | fp32_accuracy | fp32_macro_f1 | ptq_accuracy | ptq_macro_f1 | qat_accuracy | qat_macro_f1 | model_size_kb | latency_mean_ms | latency_median_ms | latency_p95_ms | deploy_gate_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E10_arduino_from_scratch | deepconv_lstm_conv2d | arduino | arduino | arduino | 20.0 | 20.0 | False | 100 | 5.0 | 0.5 | raw_no_conversion | train_zscore | True | random_stratified | arduino_from_scratch | 42 | 0.9924146649810367 | 0.9924203624956377 | 0.9532237673830595 | 0.9539966090499323 | 0.49620733249051835 | 0.47515354509578117 | 136.921875 | 4.263413499999369 | 4.252698499996654 | 4.328750499986711 | ptq=ok;qat=ok | run_id=E10_deepconv_lstm_r0; fp32_tflite=ok; ptq=ok; qat=ok; Train from scratch on Arduino train split and evaluate untouched Arduino test split. |
