# OFF_FP32_DEEPCONV_LSTM_CONV2D_E05_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/no_accel_rotation/deepconv_lstm_conv2d/e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.9824
- Macro-F1: 0.9723

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/deepconv_lstm_conv2d/e05/confusion_off_fp32_deepconv_lstm_conv2d_e05_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9937, R=0.9886, F1=0.9912, support=2723
- Jogging: P=0.9939, R=0.9962, F1=0.9950, support=2109
- Upstairs: P=0.9190, R=0.9630, F1=0.9405, support=730
- Downstairs: P=0.9637, R=0.9489, F1=0.9562, support=587
- Sitting: P=0.9895, R=0.9869, F1=0.9882, support=381
- Standing: P=0.9896, R=0.9375, F1=0.9628, support=304
