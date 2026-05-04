# OFF_FP32_DEEPCONV_LSTM_CONV2D_E06_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E06_no_norm_matched/no_accel_rotation_v2/deepconv_lstm_conv2d/e06/deepconv_lstm_conv2d_T100_Prandom_stratified_E06_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.9848
- Macro-F1: 0.9763

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/off/deepconv_lstm_conv2d/e06/confusion_off_fp32_deepconv_lstm_conv2d_e06_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9963, R=0.9930, F1=0.9947, support=2723
- Jogging: P=0.9967, R=0.9934, F1=0.9950, support=2109
- Upstairs: P=0.9443, R=0.9521, F1=0.9482, support=730
- Downstairs: P=0.9363, R=0.9523, F1=0.9443, support=587
- Sitting: P=0.9896, R=0.9948, F1=0.9921, support=381
- Standing: P=0.9868, R=0.9803, F1=0.9835, support=304
