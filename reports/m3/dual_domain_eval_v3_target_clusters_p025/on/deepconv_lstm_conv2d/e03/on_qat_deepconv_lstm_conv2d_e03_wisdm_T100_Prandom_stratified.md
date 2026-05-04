# ON_QAT_DEEPCONV_LSTM_CONV2D_E03_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E03_arduino_downsample_20hz_T100/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e03/deepconv_lstm_conv2d_T100_Prandom_stratified_E03_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.8398
- Macro-F1: 0.8078

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/deepconv_lstm_conv2d/e03/confusion_on_qat_deepconv_lstm_conv2d_e03_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9093, R=0.8436, F1=0.8752, support=2723
- Jogging: P=0.9978, R=0.8710, F1=0.9301, support=2109
- Upstairs: P=0.5276, R=0.7712, F1=0.6266, support=730
- Downstairs: P=0.6299, R=0.8177, F1=0.7116, support=587
- Sitting: P=0.8839, R=0.7795, F1=0.8285, support=381
- Standing: P=0.8775, R=0.8717, F1=0.8746, support=304
