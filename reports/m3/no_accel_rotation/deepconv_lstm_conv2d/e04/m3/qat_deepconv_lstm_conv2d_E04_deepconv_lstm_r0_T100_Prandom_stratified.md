# QAT_DEEPCONV_LSTM_CONV2D_E04_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/no_accel_rotation/deepconv_lstm_conv2d/e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.5303
- Macro-F1: 0.5411

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.252 ms/sample
- Inference latency p95: 4.307 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/no_accel_rotation/deepconv_lstm_conv2d/e04/m3/confusion_qat_deepconv_lstm_conv2d_E04_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.5208, R=0.5682, F1=0.5435, support=264
- Jogging: P=0.9770, R=0.3232, F1=0.4857, support=263
- Upstairs: P=0.2697, R=0.3636, F1=0.3097, support=264
- Downstairs: P=0.2832, R=0.4205, F1=0.3384, support=264
- Sitting: P=0.9167, R=1.0000, F1=0.9565, support=264
- Standing: P=0.7778, R=0.5057, F1=0.6129, support=263
