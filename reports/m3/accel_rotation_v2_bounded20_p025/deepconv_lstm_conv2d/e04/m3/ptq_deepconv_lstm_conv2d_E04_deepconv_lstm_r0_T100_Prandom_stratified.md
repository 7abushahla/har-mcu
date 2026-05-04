# PTQ_DEEPCONV_LSTM_CONV2D_E04_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.5594
- Macro-F1: 0.5709

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.237 ms/sample
- Inference latency p95: 4.300 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e04/m3/confusion_ptq_deepconv_lstm_conv2d_E04_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.4615, R=0.7500, F1=0.5714, support=264
- Jogging: P=0.9747, R=0.5856, F1=0.7316, support=263
- Upstairs: P=0.2581, R=0.3030, F1=0.2787, support=264
- Downstairs: P=0.2105, R=0.2121, F1=0.2113, support=264
- Sitting: P=0.9395, R=1.0000, F1=0.9688, support=264
- Standing: P=0.9638, R=0.5057, F1=0.6633, support=263
