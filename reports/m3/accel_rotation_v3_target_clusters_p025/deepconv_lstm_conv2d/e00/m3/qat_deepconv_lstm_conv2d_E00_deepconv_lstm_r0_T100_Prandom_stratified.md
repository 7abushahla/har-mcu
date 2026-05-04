# QAT_DEEPCONV_LSTM_CONV2D_E00_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e00/deepconv_lstm_conv2d_T100_Prandom_stratified_E00_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.8341
- Macro-F1: 0.8043

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.258 ms/sample
- Inference latency p95: 4.311 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e00/m3/confusion_qat_deepconv_lstm_conv2d_E00_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9134, R=0.8248, F1=0.8668, support=2723
- Jogging: P=0.9973, R=0.8687, F1=0.9285, support=2109
- Upstairs: P=0.5239, R=0.7658, F1=0.6221, support=730
- Downstairs: P=0.6010, R=0.8365, F1=0.6994, support=587
- Sitting: P=0.9104, R=0.8005, F1=0.8520, support=381
- Standing: P=0.8370, R=0.8783, F1=0.8571, support=304
