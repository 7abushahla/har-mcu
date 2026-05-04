# PTQ_DEEPCONV_LSTM_CONV2D_E00_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e00/deepconv_lstm_conv2d_T100_Prandom_stratified_E00_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.9811
- Macro-F1: 0.9710

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.246 ms/sample
- Inference latency p95: 4.328 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e00/m3/confusion_ptq_deepconv_lstm_conv2d_E00_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9945, R=0.9938, F1=0.9941, support=2723
- Jogging: P=0.9901, R=0.9943, F1=0.9922, support=2109
- Upstairs: P=0.9066, R=0.9712, F1=0.9378, support=730
- Downstairs: P=0.9791, R=0.8790, F1=0.9264, support=587
- Sitting: P=0.9869, R=0.9869, F1=0.9869, support=381
- Standing: P=0.9869, R=0.9901, F1=0.9885, support=304
