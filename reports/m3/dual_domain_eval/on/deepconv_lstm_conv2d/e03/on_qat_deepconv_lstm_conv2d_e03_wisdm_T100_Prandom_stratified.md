# ON_QAT_DEEPCONV_LSTM_CONV2D_E03_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E03_arduino_downsample_20hz_T100/accel_rotation/deepconv_lstm_conv2d/e03/deepconv_lstm_conv2d_T100_Prandom_stratified_E03_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.4102
- Macro-F1: 0.2884

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/deepconv_lstm_conv2d/e03/confusion_on_qat_deepconv_lstm_conv2d_e03_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.7468, R=0.3195, F1=0.4475, support=2723
- Jogging: P=0.9293, R=0.5045, F1=0.6540, support=2109
- Upstairs: P=0.1908, R=0.6397, F1=0.2940, support=730
- Downstairs: P=0.1908, R=0.6729, F1=0.2973, support=587
- Sitting: P=1.0000, R=0.0157, F1=0.0310, support=381
- Standing: P=1.0000, R=0.0033, F1=0.0066, support=304
