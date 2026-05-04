# OFF_PTQ_DEEPCONV_LSTM_CONV2D_E04_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/no_accel_rotation/deepconv_lstm_conv2d/e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.5632
- Macro-F1: 0.5916

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/deepconv_lstm_conv2d/e04/confusion_off_ptq_deepconv_lstm_conv2d_e04_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.8036, R=0.5114, F1=0.6250, support=264
- Jogging: P=1.0000, R=0.5323, F1=0.6948, support=263
- Upstairs: P=0.2366, R=0.3333, F1=0.2767, support=264
- Downstairs: P=0.3067, R=0.6098, F1=0.4081, support=264
- Sitting: P=0.9742, R=1.0000, F1=0.9869, support=264
- Standing: P=0.9717, R=0.3916, F1=0.5583, support=263
