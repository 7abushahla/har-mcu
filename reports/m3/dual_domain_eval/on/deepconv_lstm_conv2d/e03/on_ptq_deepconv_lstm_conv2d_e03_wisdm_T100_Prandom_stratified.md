# ON_PTQ_DEEPCONV_LSTM_CONV2D_E03_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E03_arduino_downsample_20hz_T100/accel_rotation/deepconv_lstm_conv2d/e03/deepconv_lstm_conv2d_T100_Prandom_stratified_E03_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.9444
- Macro-F1: 0.8919

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/deepconv_lstm_conv2d/e03/confusion_on_ptq_deepconv_lstm_conv2d_e03_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9893, R=0.9893, F1=0.9893, support=2723
- Jogging: P=0.9937, R=0.9749, F1=0.9842, support=2109
- Upstairs: P=0.7043, R=0.9562, F1=0.8112, support=730
- Downstairs: P=0.9351, R=0.8586, F1=0.8952, support=587
- Sitting: P=0.9931, R=0.7585, F1=0.8601, support=381
- Standing: P=0.9638, R=0.7007, F1=0.8114, support=304
