# OFF_QAT_DEEPCONV_LSTM_CONV2D_E04_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/no_accel_rotation_v2/deepconv_lstm_conv2d/e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.5316
- Macro-F1: 0.5370

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/off/deepconv_lstm_conv2d/e04/confusion_off_qat_deepconv_lstm_conv2d_e04_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.5177, R=0.6098, F1=0.5600, support=264
- Jogging: P=1.0000, R=0.3384, F1=0.5057, support=263
- Upstairs: P=0.2920, R=0.3030, F1=0.2974, support=264
- Downstairs: P=0.2736, R=0.4394, F1=0.3372, support=264
- Sitting: P=0.8771, R=1.0000, F1=0.9345, support=264
- Standing: P=0.7158, R=0.4981, F1=0.5874, support=263
