# QAT_DEEPCONV_LSTM_CONV2D_E07_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E07_skip_inference_norm_diag/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e07/deepconv_lstm_conv2d_T100_Prandom_stratified_E07_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.1694
- Macro-F1: 0.0671

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.250 ms/sample
- Inference latency p95: 4.306 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e07/m3/confusion_qat_deepconv_lstm_conv2d_E07_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.0000, R=0.0000, F1=0.0000, support=264
- Jogging: P=0.0000, R=0.0000, F1=0.0000, support=263
- Upstairs: P=0.1826, R=0.0795, F1=0.1108, support=264
- Downstairs: P=0.1678, R=0.9318, F1=0.2844, support=264
- Sitting: P=0.0000, R=0.0000, F1=0.0000, support=264
- Standing: P=1.0000, R=0.0038, F1=0.0076, support=263
