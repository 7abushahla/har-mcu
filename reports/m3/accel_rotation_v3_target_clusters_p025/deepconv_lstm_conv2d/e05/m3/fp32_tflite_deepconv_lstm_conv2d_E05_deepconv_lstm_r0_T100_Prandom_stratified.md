# FP32_TFLITE_DEEPCONV_LSTM_CONV2D_E05_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.5202
- Macro-F1: 0.4515

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 0.651 ms/sample
- Inference latency p95: 0.678 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e05/m3/confusion_fp32_tflite_deepconv_lstm_conv2d_E05_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.2667, R=0.0152, F1=0.0287, support=264
- Jogging: P=0.8901, R=0.6464, F1=0.7489, support=263
- Upstairs: P=0.3015, R=0.9205, F1=0.4542, support=264
- Downstairs: P=0.2500, R=0.0114, F1=0.0217, support=264
- Sitting: P=0.6600, R=1.0000, F1=0.7952, support=264
- Standing: P=0.8797, R=0.5285, F1=0.6603, support=263
