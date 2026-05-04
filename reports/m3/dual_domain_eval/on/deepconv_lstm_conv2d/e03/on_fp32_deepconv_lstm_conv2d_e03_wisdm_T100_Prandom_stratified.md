# ON_FP32_DEEPCONV_LSTM_CONV2D_E03_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E03_arduino_downsample_20hz_T100/accel_rotation/deepconv_lstm_conv2d/e03/deepconv_lstm_conv2d_T100_Prandom_stratified_E03_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.9450
- Macro-F1: 0.8941

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/deepconv_lstm_conv2d/e03/confusion_on_fp32_deepconv_lstm_conv2d_e03_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9901, R=0.9886, F1=0.9893, support=2723
- Jogging: P=0.9937, R=0.9749, F1=0.9842, support=2109
- Upstairs: P=0.7046, R=0.9575, F1=0.8118, support=730
- Downstairs: P=0.9351, R=0.8586, F1=0.8952, support=587
- Sitting: P=0.9966, R=0.7664, F1=0.8665, support=381
- Standing: P=0.9685, R=0.7072, F1=0.8175, support=304
