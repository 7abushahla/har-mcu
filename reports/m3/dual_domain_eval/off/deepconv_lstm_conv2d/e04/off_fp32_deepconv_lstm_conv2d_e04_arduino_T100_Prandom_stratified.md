# OFF_FP32_DEEPCONV_LSTM_CONV2D_E04_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/no_accel_rotation/deepconv_lstm_conv2d/e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.5670
- Macro-F1: 0.5949

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/deepconv_lstm_conv2d/e04/confusion_off_fp32_deepconv_lstm_conv2d_e04_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.8333, R=0.5114, F1=0.6338, support=264
- Jogging: P=1.0000, R=0.5627, F1=0.7202, support=263
- Upstairs: P=0.2287, R=0.3258, F1=0.2687, support=264
- Downstairs: P=0.3160, R=0.6212, F1=0.4189, support=264
- Sitting: P=0.9635, R=1.0000, F1=0.9814, support=264
- Standing: P=0.9709, R=0.3802, F1=0.5464, support=263
