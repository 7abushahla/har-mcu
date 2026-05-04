# OFF_FP32_DEEPCONV_LSTM_CONV2D_E04_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/no_accel_rotation/deepconv_lstm_conv2d/e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.9763
- Macro-F1: 0.9589

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/deepconv_lstm_conv2d/e04/confusion_off_fp32_deepconv_lstm_conv2d_e04_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9901, R=0.9897, F1=0.9899, support=2723
- Jogging: P=0.9943, R=0.9943, F1=0.9943, support=2109
- Upstairs: P=0.8689, R=0.9712, F1=0.9172, support=730
- Downstairs: P=0.9781, R=0.9131, F1=0.9445, support=587
- Sitting: P=0.9947, R=0.9869, F1=0.9908, support=381
- Standing: P=0.9923, R=0.8520, F1=0.9168, support=304
