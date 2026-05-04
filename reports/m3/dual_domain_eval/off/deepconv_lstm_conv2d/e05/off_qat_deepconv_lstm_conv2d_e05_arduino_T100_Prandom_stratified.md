# OFF_QAT_DEEPCONV_LSTM_CONV2D_E05_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/no_accel_rotation/deepconv_lstm_conv2d/e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.5183
- Macro-F1: 0.5295

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/deepconv_lstm_conv2d/e05/confusion_off_qat_deepconv_lstm_conv2d_e05_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.5517, R=0.5455, F1=0.5486, support=264
- Jogging: P=1.0000, R=0.3194, F1=0.4841, support=263
- Upstairs: P=0.2444, R=0.3295, F1=0.2806, support=264
- Downstairs: P=0.2807, R=0.4508, F1=0.3459, support=264
- Sitting: P=0.8859, R=1.0000, F1=0.9395, support=264
- Standing: P=0.7673, R=0.4639, F1=0.5782, support=263
