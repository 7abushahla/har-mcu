# OFF_QAT_DEEPCONV_LSTM_CONV2D_E05_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/no_accel_rotation_v2/deepconv_lstm_conv2d/e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.8316
- Macro-F1: 0.7849

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/off/deepconv_lstm_conv2d/e05/confusion_off_qat_deepconv_lstm_conv2d_e05_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9446, R=0.8898, F1=0.9164, support=2723
- Jogging: P=0.9825, R=0.7975, F1=0.8804, support=2109
- Upstairs: P=0.5371, R=0.7740, F1=0.6341, support=730
- Downstairs: P=0.5426, R=0.6405, F1=0.5875, support=587
- Sitting: P=0.8252, R=0.9790, F1=0.8956, support=381
- Standing: P=0.7333, R=0.8684, F1=0.7952, support=304
