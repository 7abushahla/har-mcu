# OFF_PTQ_DEEPCONV_LSTM_CONV2D_E10_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E10_arduino_from_scratch/no_accel_rotation/deepconv_lstm_conv2d/e10/deepconv_lstm_conv2d_T100_Prandom_stratified_E10_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.3228
- Macro-F1: 0.1721

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/deepconv_lstm_conv2d/e10/confusion_off_ptq_deepconv_lstm_conv2d_e10_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.0000, R=0.0000, F1=0.0000, support=2723
- Jogging: P=0.3576, R=0.8815, F1=0.5088, support=2109
- Upstairs: P=0.1883, R=0.1767, F1=0.1823, support=730
- Downstairs: P=0.2381, R=0.0085, F1=0.0164, support=587
- Sitting: P=0.2290, R=0.5591, F1=0.3249, support=381
- Standing: P=0.0000, R=0.0000, F1=0.0000, support=304
