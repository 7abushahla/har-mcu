# OFF_QAT_DEEPCONV_LSTM_CONV2D_E06_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E06_no_norm_matched/no_accel_rotation_v2/deepconv_lstm_conv2d/e06/deepconv_lstm_conv2d_T100_Prandom_stratified_E06_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.2035
- Macro-F1: 0.1151

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/off/deepconv_lstm_conv2d/e06/confusion_off_qat_deepconv_lstm_conv2d_e06_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.5333, R=0.0303, F1=0.0573, support=264
- Jogging: P=0.0000, R=0.0000, F1=0.0000, support=263
- Upstairs: P=0.0847, R=0.0379, F1=0.0524, support=264
- Downstairs: P=0.1752, R=0.3106, F1=0.2240, support=264
- Sitting: P=0.0000, R=0.0000, F1=0.0000, support=264
- Standing: P=0.2263, R=0.8441, F1=0.3569, support=263
