# OFF_FP32_DEEPCONV_LSTM_CONV2D_E04_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/no_accel_rotation_v2/deepconv_lstm_conv2d/e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.5607
- Macro-F1: 0.5734

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/off/deepconv_lstm_conv2d/e04/confusion_off_fp32_deepconv_lstm_conv2d_e04_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.5099, R=0.5833, F1=0.5442, support=264
- Jogging: P=1.0000, R=0.4791, F1=0.6478, support=263
- Upstairs: P=0.2852, R=0.2765, F1=0.2808, support=264
- Downstairs: P=0.3168, R=0.5795, F1=0.4096, support=264
- Sitting: P=0.9395, R=1.0000, F1=0.9688, support=264
- Standing: P=0.8731, R=0.4449, F1=0.5894, support=263
