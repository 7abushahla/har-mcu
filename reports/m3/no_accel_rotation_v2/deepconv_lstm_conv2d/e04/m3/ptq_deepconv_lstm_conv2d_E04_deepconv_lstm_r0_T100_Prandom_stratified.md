# PTQ_DEEPCONV_LSTM_CONV2D_E04_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/no_accel_rotation_v2/deepconv_lstm_conv2d/e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.5537
- Macro-F1: 0.5662

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.244 ms/sample
- Inference latency p95: 4.273 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/no_accel_rotation_v2/deepconv_lstm_conv2d/e04/m3/confusion_ptq_deepconv_lstm_conv2d_E04_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.4952, R=0.5833, F1=0.5357, support=264
- Jogging: P=1.0000, R=0.4639, F1=0.6338, support=263
- Upstairs: P=0.2892, R=0.2727, F1=0.2807, support=264
- Downstairs: P=0.3075, R=0.5720, F1=0.4000, support=264
- Sitting: P=0.9429, R=1.0000, F1=0.9706, support=264
- Standing: P=0.8760, R=0.4297, F1=0.5765, support=263
