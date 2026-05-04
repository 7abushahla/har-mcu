# QAT_DEEPCONV_LSTM_CONV2D_E04_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.5335
- Macro-F1: 0.5355

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.243 ms/sample
- Inference latency p95: 4.288 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e04/m3/confusion_qat_deepconv_lstm_conv2d_E04_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.6678, R=0.7614, F1=0.7115, support=264
- Jogging: P=0.8700, R=0.3308, F1=0.4793, support=263
- Upstairs: P=0.1672, R=0.1970, F1=0.1809, support=264
- Downstairs: P=0.2892, R=0.4053, F1=0.3375, support=264
- Sitting: P=0.7586, R=1.0000, F1=0.8627, support=264
- Standing: P=0.8750, R=0.5057, F1=0.6410, support=263
