# OFF_FP32_DEEPCONV_LSTM_CONV2D_E05_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/no_accel_rotation/deepconv_lstm_conv2d/e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.5777
- Macro-F1: 0.6043

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/deepconv_lstm_conv2d/e05/confusion_off_fp32_deepconv_lstm_conv2d_e05_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.8497, R=0.4924, F1=0.6235, support=264
- Jogging: P=0.9934, R=0.5703, F1=0.7246, support=263
- Upstairs: P=0.2278, R=0.2917, F1=0.2558, support=264
- Downstairs: P=0.3254, R=0.6705, F1=0.4381, support=264
- Sitting: P=0.9565, R=1.0000, F1=0.9778, support=264
- Standing: P=0.9667, R=0.4411, F1=0.6057, support=263
