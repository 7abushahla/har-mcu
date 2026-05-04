# ON_QAT_DEEPCONV_LSTM_CONV2D_E03_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E03_arduino_downsample_20hz_T100/accel_rotation/deepconv_lstm_conv2d/e03/deepconv_lstm_conv2d_T100_Prandom_stratified_E03_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.1675
- Macro-F1: 0.0493

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/deepconv_lstm_conv2d/e03/confusion_on_qat_deepconv_lstm_conv2d_e03_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.1685, R=1.0000, F1=0.2884, support=264
- Jogging: P=0.0000, R=0.0000, F1=0.0000, support=263
- Upstairs: P=0.5000, R=0.0038, F1=0.0075, support=264
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=264
- Sitting: P=0.0000, R=0.0000, F1=0.0000, support=264
- Standing: P=0.0000, R=0.0000, F1=0.0000, support=263
