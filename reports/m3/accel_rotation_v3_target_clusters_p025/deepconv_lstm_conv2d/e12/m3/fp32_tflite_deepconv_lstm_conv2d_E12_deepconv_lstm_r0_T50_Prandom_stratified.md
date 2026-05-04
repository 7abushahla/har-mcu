# FP32_TFLITE_DEEPCONV_LSTM_CONV2D_E12_DEEPCONV_LSTM_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e12/deepconv_lstm_conv2d_T50_Prandom_stratified_E12_deepconv_lstm_r0_fp32.tflite`
- Model size: 396.43 KB
- Accuracy: 0.9470
- Macro-F1: 0.9474

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 0.311 ms/sample
- Inference latency p95: 0.332 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e12/m3/confusion_fp32_tflite_deepconv_lstm_conv2d_E12_deepconv_lstm_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9861, R=0.9357, F1=0.9602, support=529
- Jogging: P=0.9845, R=0.9640, F1=0.9742, support=528
- Upstairs: P=0.8848, R=0.8998, F1=0.8922, support=529
- Downstairs: P=0.8621, R=0.8996, F1=0.8804, support=528
- Sitting: P=0.9962, R=0.9830, F1=0.9895, support=528
- Standing: P=0.9760, R=1.0000, F1=0.9878, support=528
