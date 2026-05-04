# QAT_DEEPCONV_LSTM_CONV2D_E12_DEEPCONV_LSTM_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/accel_rotation/deepconv_lstm_conv2d/e12/deepconv_lstm_conv2d_T50_Prandom_stratified_E12_deepconv_lstm_r0_qat.tflite`
- Model size: 108.05 KB
- Accuracy: 0.4719
- Macro-F1: 0.4951

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 2.042 ms/sample
- Inference latency p95: 2.081 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/accel_rotation/deepconv_lstm_conv2d/e12/m3/confusion_qat_deepconv_lstm_conv2d_E12_deepconv_lstm_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.5974, R=0.5217, F1=0.5570, support=529
- Jogging: P=0.8560, R=0.6193, F1=0.7187, support=528
- Upstairs: P=0.2338, R=0.5784, F1=0.3330, support=529
- Downstairs: P=0.3636, R=0.4621, F1=0.4070, support=528
- Sitting: P=0.9873, R=0.4413, F1=0.6099, support=528
- Standing: P=1.0000, R=0.2083, F1=0.3448, support=528
