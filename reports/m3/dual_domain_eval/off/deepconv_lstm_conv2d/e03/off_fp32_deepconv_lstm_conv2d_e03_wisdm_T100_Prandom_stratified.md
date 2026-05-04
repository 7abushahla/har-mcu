# OFF_FP32_DEEPCONV_LSTM_CONV2D_E03_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E03_arduino_downsample_20hz_T100/no_accel_rotation/deepconv_lstm_conv2d/e03/deepconv_lstm_conv2d_T100_Prandom_stratified_E03_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.9792
- Macro-F1: 0.9701

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/deepconv_lstm_conv2d/e03/confusion_off_fp32_deepconv_lstm_conv2d_e03_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9941, R=0.9849, F1=0.9895, support=2723
- Jogging: P=0.9957, R=0.9905, F1=0.9931, support=2109
- Upstairs: P=0.8920, R=0.9616, F1=0.9255, support=730
- Downstairs: P=0.9645, R=0.9267, F1=0.9453, support=587
- Sitting: P=0.9818, R=0.9895, F1=0.9856, support=381
- Standing: P=0.9835, R=0.9803, F1=0.9819, support=304
