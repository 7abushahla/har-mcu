# OFF_QAT_DEEPCONV_LSTM_CONV2D_E04_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/no_accel_rotation/deepconv_lstm_conv2d/e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.9464
- Macro-F1: 0.9166

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/deepconv_lstm_conv2d/e04/confusion_off_qat_deepconv_lstm_conv2d_e04_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9816, R=0.9813, F1=0.9815, support=2723
- Jogging: P=0.9995, R=0.9569, F1=0.9777, support=2109
- Upstairs: P=0.7468, R=0.9452, F1=0.8343, support=730
- Downstairs: P=0.8964, R=0.7666, F1=0.8264, support=587
- Sitting: P=0.9736, R=0.9685, F1=0.9711, support=381
- Standing: P=0.9340, R=0.8849, F1=0.9088, support=304
