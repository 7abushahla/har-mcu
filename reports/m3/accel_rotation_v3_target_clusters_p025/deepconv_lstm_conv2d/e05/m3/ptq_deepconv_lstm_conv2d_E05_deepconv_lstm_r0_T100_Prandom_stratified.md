# PTQ_DEEPCONV_LSTM_CONV2D_E05_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.5076
- Macro-F1: 0.4404

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.257 ms/sample
- Inference latency p95: 4.340 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e05/m3/confusion_ptq_deepconv_lstm_conv2d_E05_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.2143, R=0.0114, F1=0.0216, support=264
- Jogging: P=0.8603, R=0.5856, F1=0.6968, support=263
- Upstairs: P=0.2943, R=0.9129, F1=0.4451, support=264
- Downstairs: P=0.1875, R=0.0114, F1=0.0214, support=264
- Sitting: P=0.6584, R=1.0000, F1=0.7940, support=264
- Standing: P=0.9020, R=0.5247, F1=0.6635, support=263
