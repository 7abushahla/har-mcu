# OFF_FP32_DEEPCONV_LSTM_CONV2D_E12_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/no_accel_rotation_v2/deepconv_lstm_conv2d/e12/deepconv_lstm_conv2d_T50_Prandom_stratified_E12_deepconv_lstm_r0_fp32.tflite`
- Model size: 396.43 KB
- Accuracy: 0.3029
- Macro-F1: 0.1379

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/off/deepconv_lstm_conv2d/e12/confusion_off_fp32_deepconv_lstm_conv2d_e12_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.1930, R=0.0503, F1=0.0799, support=5482
- Jogging: P=0.3842, R=0.8191, F1=0.5230, support=4250
- Upstairs: P=0.1364, R=0.2842, F1=0.1843, support=1541
- Downstairs: P=0.0802, R=0.0104, F1=0.0184, support=1249
- Sitting: P=0.1525, R=0.0116, F1=0.0215, support=777
- Standing: P=0.0000, R=0.0000, F1=0.0000, support=624
