# OFF_QAT_DEEPCONV_LSTM_CONV2D_E05_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/no_accel_rotation/deepconv_lstm_conv2d/e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.9526
- Macro-F1: 0.9276

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/deepconv_lstm_conv2d/e05/confusion_off_qat_deepconv_lstm_conv2d_e05_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9831, R=0.9824, F1=0.9827, support=2723
- Jogging: P=0.9995, R=0.9592, F1=0.9789, support=2109
- Upstairs: P=0.7738, R=0.9562, F1=0.8554, support=730
- Downstairs: P=0.9103, R=0.7956, F1=0.8491, support=587
- Sitting: P=0.9735, R=0.9659, F1=0.9697, support=381
- Standing: P=0.9426, R=0.9178, F1=0.9300, support=304
