# OFF_QAT_DEEPCONV_LSTM_CONV2D_E03_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E03_arduino_downsample_20hz_T100/no_accel_rotation/deepconv_lstm_conv2d/e03/deepconv_lstm_conv2d_T100_Prandom_stratified_E03_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.8395
- Macro-F1: 0.7843

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/deepconv_lstm_conv2d/e03/confusion_off_qat_deepconv_lstm_conv2d_e03_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9569, R=0.8961, F1=0.9255, support=2723
- Jogging: P=0.9796, R=0.8193, F1=0.8923, support=2109
- Upstairs: P=0.5586, R=0.7699, F1=0.6475, support=730
- Downstairs: P=0.5530, R=0.6491, F1=0.5972, support=587
- Sitting: P=0.7979, R=0.9843, F1=0.8813, support=381
- Standing: P=0.7070, R=0.8257, F1=0.7618, support=304
