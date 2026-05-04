# FP32_TFLITE_DEEPCONV_LSTM_CONV2D_E08_DEEPCONV_LSTM_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E08_T50_window/no_accel_rotation/deepconv_lstm_conv2d/e08/deepconv_lstm_conv2d_T50_Prandom_stratified_E08_deepconv_lstm_r0_fp32.tflite`
- Model size: 396.43 KB
- Accuracy: 0.1669
- Macro-F1: 0.0477

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 0.308 ms/sample
- Inference latency p95: 0.329 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/no_accel_rotation/deepconv_lstm_conv2d/e08/m3/confusion_fp32_tflite_deepconv_lstm_conv2d_E08_deepconv_lstm_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.1669, R=1.0000, F1=0.2860, support=529
- Jogging: P=0.0000, R=0.0000, F1=0.0000, support=528
- Upstairs: P=0.0000, R=0.0000, F1=0.0000, support=529
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=528
- Sitting: P=0.0000, R=0.0000, F1=0.0000, support=528
- Standing: P=0.0000, R=0.0000, F1=0.0000, support=528
