# FP32_TFLITE_DEEPCONV_LSTM_CONV2D_E04_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.5613
- Macro-F1: 0.5714

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 0.647 ms/sample
- Inference latency p95: 0.669 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e04/m3/confusion_fp32_tflite_deepconv_lstm_conv2d_E04_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.4605, R=0.7500, F1=0.5706, support=264
- Jogging: P=0.9704, R=0.6236, F1=0.7593, support=263
- Upstairs: P=0.2557, R=0.2955, F1=0.2742, support=264
- Downstairs: P=0.1984, R=0.1932, F1=0.1958, support=264
- Sitting: P=0.9329, R=1.0000, F1=0.9653, support=264
- Standing: P=0.9638, R=0.5057, F1=0.6633, support=263
