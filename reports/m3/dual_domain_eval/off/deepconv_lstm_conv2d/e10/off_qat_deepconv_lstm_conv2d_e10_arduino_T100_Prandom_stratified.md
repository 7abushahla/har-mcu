# OFF_QAT_DEEPCONV_LSTM_CONV2D_E10_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E10_arduino_from_scratch/no_accel_rotation/deepconv_lstm_conv2d/e10/deepconv_lstm_conv2d_T100_Prandom_stratified_E10_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.3647
- Macro-F1: 0.3411

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/deepconv_lstm_conv2d/e10/confusion_off_qat_deepconv_lstm_conv2d_e10_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.3831, R=0.8068, F1=0.5195, support=264
- Jogging: P=1.0000, R=0.0608, F1=0.1147, support=263
- Upstairs: P=0.1535, R=0.2652, F1=0.1944, support=264
- Downstairs: P=0.3899, R=0.4962, F1=0.4367, support=264
- Sitting: P=1.0000, R=0.2197, F1=0.3602, support=264
- Standing: P=0.5563, R=0.3384, F1=0.4208, support=263
