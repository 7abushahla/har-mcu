# FP32_TFLITE_DEEPCONV_LSTM_CONV2D_E04_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/accel_rotation/deepconv_lstm_conv2d/e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.5455
- Macro-F1: 0.5178

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 0.649 ms/sample
- Inference latency p95: 0.676 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/accel_rotation/deepconv_lstm_conv2d/e04/m3/confusion_fp32_tflite_deepconv_lstm_conv2d_E04_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.2617, R=0.2538, F1=0.2577, support=264
- Jogging: P=0.6862, R=0.9810, F1=0.8075, support=263
- Upstairs: P=0.2783, R=0.3636, F1=0.3153, support=264
- Downstairs: P=0.4667, R=0.1326, F1=0.2065, support=264
- Sitting: P=0.6824, R=0.9848, F1=0.8062, support=264
- Standing: P=0.9866, R=0.5589, F1=0.7136, support=263
