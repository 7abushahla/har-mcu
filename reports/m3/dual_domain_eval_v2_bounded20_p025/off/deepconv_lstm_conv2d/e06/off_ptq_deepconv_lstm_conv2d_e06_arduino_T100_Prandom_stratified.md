# OFF_PTQ_DEEPCONV_LSTM_CONV2D_E06_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E06_no_norm_matched/no_accel_rotation_v2/deepconv_lstm_conv2d/e06/deepconv_lstm_conv2d_T100_Prandom_stratified_E06_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.2137
- Macro-F1: 0.1542

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/off/deepconv_lstm_conv2d/e06/confusion_off_ptq_deepconv_lstm_conv2d_e06_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.3451, R=0.1477, F1=0.2069, support=264
- Jogging: P=0.0000, R=0.0000, F1=0.0000, support=263
- Upstairs: P=0.1505, R=0.1591, F1=0.1547, support=264
- Downstairs: P=0.1866, R=0.2538, F1=0.2151, support=264
- Sitting: P=0.0000, R=0.0000, F1=0.0000, support=264
- Standing: P=0.2297, R=0.7224, F1=0.3486, support=263
