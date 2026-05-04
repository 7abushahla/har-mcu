# OFF_QAT_DEEPCONV_LSTM_CONV2D_E10_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E10_arduino_from_scratch/no_accel_rotation_v2/deepconv_lstm_conv2d/e10/deepconv_lstm_conv2d_T100_Prandom_stratified_E10_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.4260
- Macro-F1: 0.4101

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/off/deepconv_lstm_conv2d/e10/confusion_off_qat_deepconv_lstm_conv2d_e10_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.5374, R=0.7083, F1=0.6111, support=264
- Jogging: P=1.0000, R=0.2890, F1=0.4484, support=263
- Upstairs: P=0.1504, R=0.2803, F1=0.1958, support=264
- Downstairs: P=0.3943, R=0.5720, F1=0.4668, support=264
- Sitting: P=1.0000, R=0.0455, F1=0.0870, support=264
- Standing: P=0.6421, R=0.6616, F1=0.6517, support=263
