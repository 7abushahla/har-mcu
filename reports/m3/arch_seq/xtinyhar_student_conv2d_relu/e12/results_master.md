# Master Results

- Total rows: `1`

| paper_slug | protocol | variant | run_id | run_mode | compression_focus | accuracy | macro_f1 | ptq_status | qat_status | train_device | eval_fp32_device | ptq_device | eval_ptq_device | qat_device | eval_qat_device | fp32_training_time_sec | fp32_model_size_kb | fp32_tflite_status | fp32_tflite_eval_status | fp32_tflite_accuracy | fp32_tflite_macro_f1 | qat_training_time_sec | ptq_inference_latency_ms_median | ptq_inference_latency_ms_p95 | qat_inference_latency_ms_median | qat_inference_latency_ms_p95 | ptq_model_size_kb | qat_model_size_kb | paper_target_score | delta_vs_paper | notes_assumptions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| m3 | random_stratified | xtinyhar_student_conv2d_relu | E12_xtinyhar_student_conv2d_relu_r0 | sanity_check | ptq_qat_only | 0.9558359621451105 | 0.955712688927366 | ok | ok | gpu | gpu | gpu | gpu | cpu | cpu | 30.138414282999975 | 1086.16015625 | ok | ok | 0.9555205047318612 | 0.9554112335982178 | 15.922920617000045 | 0.31880500006309376 | 0.33903749996966326 | 0.32254499996042796 | 0.34500250001201493 | 308.6171875 | 309.0703125 | — | — | — |

