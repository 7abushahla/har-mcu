# QAT_DEEPCONV_LSTM_CONV2D_E05_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.5442
- Macro-F1: 0.5485

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.246 ms/sample
- Inference latency p95: 4.308 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e05/m3/confusion_qat_deepconv_lstm_conv2d_E05_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.5982, R=0.7727, F1=0.6744, support=264
- Jogging: P=0.8276, R=0.3650, F1=0.5066, support=263
- Upstairs: P=0.2040, R=0.2311, F1=0.2167, support=264
- Downstairs: P=0.2799, R=0.3902, F1=0.3259, support=264
- Sitting: P=0.8354, R=1.0000, F1=0.9103, support=264
- Standing: P=0.9366, R=0.5057, F1=0.6568, support=263
