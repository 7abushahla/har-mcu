# OFF_QAT_DEEPCONV_LSTM_CONV2D_E03_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E03_arduino_downsample_20hz_T100/no_accel_rotation_v2/deepconv_lstm_conv2d/e03/deepconv_lstm_conv2d_T100_Prandom_stratified_E03_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.8301
- Macro-F1: 0.7784

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/off/deepconv_lstm_conv2d/e03/confusion_off_qat_deepconv_lstm_conv2d_e03_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9465, R=0.8832, F1=0.9138, support=2723
- Jogging: P=0.9832, R=0.8061, F1=0.8859, support=2109
- Upstairs: P=0.5345, R=0.7630, F1=0.6287, support=730
- Downstairs: P=0.5510, R=0.6627, F1=0.6017, support=587
- Sitting: P=0.8082, R=0.9843, F1=0.8876, support=381
- Standing: P=0.7017, R=0.8125, F1=0.7530, support=304
