# ON_PTQ_DEEPCONV_LSTM_CONV2D_E07_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E07_skip_inference_norm_diag/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e07/deepconv_lstm_conv2d_T100_Prandom_stratified_E07_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.9801
- Macro-F1: 0.9682

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/deepconv_lstm_conv2d/e07/confusion_on_ptq_deepconv_lstm_conv2d_e07_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9949, R=0.9945, F1=0.9947, support=2723
- Jogging: P=0.9915, R=0.9953, F1=0.9934, support=2109
- Upstairs: P=0.8941, R=0.9712, F1=0.9311, support=730
- Downstairs: P=0.9787, R=0.8620, F1=0.9167, support=587
- Sitting: P=0.9894, R=0.9843, F1=0.9868, support=381
- Standing: P=0.9837, R=0.9901, F1=0.9869, support=304
