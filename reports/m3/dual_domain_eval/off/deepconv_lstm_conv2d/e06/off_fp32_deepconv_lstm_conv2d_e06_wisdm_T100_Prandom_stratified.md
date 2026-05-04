# OFF_FP32_DEEPCONV_LSTM_CONV2D_E06_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E06_no_norm_matched/no_accel_rotation/deepconv_lstm_conv2d/e06/deepconv_lstm_conv2d_T100_Prandom_stratified_E06_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.9842
- Macro-F1: 0.9762

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/deepconv_lstm_conv2d/e06/confusion_off_fp32_deepconv_lstm_conv2d_e06_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9952, R=0.9927, F1=0.9939, support=2723
- Jogging: P=0.9981, R=0.9905, F1=0.9943, support=2109
- Upstairs: P=0.9284, R=0.9589, F1=0.9434, support=730
- Downstairs: P=0.9521, R=0.9472, F1=0.9496, support=587
- Sitting: P=0.9870, R=0.9948, F1=0.9908, support=381
- Standing: P=0.9868, R=0.9836, F1=0.9852, support=304
