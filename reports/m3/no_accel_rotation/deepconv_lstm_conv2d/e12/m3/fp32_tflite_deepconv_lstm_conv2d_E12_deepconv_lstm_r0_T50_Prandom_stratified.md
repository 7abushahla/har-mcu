# FP32_TFLITE_DEEPCONV_LSTM_CONV2D_E12_DEEPCONV_LSTM_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/no_accel_rotation/deepconv_lstm_conv2d/e12/deepconv_lstm_conv2d_T50_Prandom_stratified_E12_deepconv_lstm_r0_fp32.tflite`
- Model size: 396.43 KB
- Accuracy: 0.8943
- Macro-F1: 0.8979

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 0.311 ms/sample
- Inference latency p95: 0.321 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/no_accel_rotation/deepconv_lstm_conv2d/e12/m3/confusion_fp32_tflite_deepconv_lstm_conv2d_E12_deepconv_lstm_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9632, R=0.8412, F1=0.8981, support=529
- Jogging: P=0.9920, R=0.9451, F1=0.9680, support=528
- Upstairs: P=0.6689, R=0.9471, F1=0.7840, support=529
- Downstairs: P=0.8837, R=0.8636, F1=0.8736, support=528
- Sitting: P=0.9944, R=1.0000, F1=0.9972, support=528
- Standing: P=0.9927, R=0.7689, F1=0.8666, support=528
