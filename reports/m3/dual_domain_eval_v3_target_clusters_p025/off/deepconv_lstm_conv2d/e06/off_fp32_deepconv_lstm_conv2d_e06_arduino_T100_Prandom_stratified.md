# OFF_FP32_DEEPCONV_LSTM_CONV2D_E06_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E06_no_norm_matched/no_accel_rotation_v2/deepconv_lstm_conv2d/e06/deepconv_lstm_conv2d_T100_Prandom_stratified_E06_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.2016
- Macro-F1: 0.1442

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/off/deepconv_lstm_conv2d/e06/confusion_off_fp32_deepconv_lstm_conv2d_e06_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.3252, R=0.1515, F1=0.2067, support=264
- Jogging: P=0.0000, R=0.0000, F1=0.0000, support=263
- Upstairs: P=0.1339, R=0.1136, F1=0.1230, support=264
- Downstairs: P=0.1831, R=0.2538, F1=0.2127, support=264
- Sitting: P=0.0000, R=0.0000, F1=0.0000, support=264
- Standing: P=0.2104, R=0.6920, F1=0.3227, support=263
