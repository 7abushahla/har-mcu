# ON_FP32_DEEPCONV_LSTM_CONV2D_E00_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e00/deepconv_lstm_conv2d_T100_Prandom_stratified_E00_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.9813
- Macro-F1: 0.9708

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/deepconv_lstm_conv2d/e00/confusion_on_fp32_deepconv_lstm_conv2d_e00_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9941, R=0.9938, F1=0.9939, support=2723
- Jogging: P=0.9906, R=0.9943, F1=0.9924, support=2109
- Upstairs: P=0.9100, R=0.9699, F1=0.9390, support=730
- Downstairs: P=0.9793, R=0.8859, F1=0.9302, support=587
- Sitting: P=0.9868, R=0.9816, F1=0.9842, support=381
- Standing: P=0.9805, R=0.9901, F1=0.9853, support=304
