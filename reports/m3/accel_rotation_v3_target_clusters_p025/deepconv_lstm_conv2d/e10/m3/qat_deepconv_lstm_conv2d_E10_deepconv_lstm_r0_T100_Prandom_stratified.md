# QAT_DEEPCONV_LSTM_CONV2D_E10_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E10_arduino_from_scratch/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e10/deepconv_lstm_conv2d_T100_Prandom_stratified_E10_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.5335
- Macro-F1: 0.5152

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.254 ms/sample
- Inference latency p95: 4.344 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e10/m3/confusion_qat_deepconv_lstm_conv2d_E10_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.5499, R=0.7311, F1=0.6276, support=264
- Jogging: P=1.0000, R=0.2700, F1=0.4251, support=263
- Upstairs: P=0.3904, R=0.4318, F1=0.4101, support=264
- Downstairs: P=0.4049, R=0.8068, F1=0.5392, support=264
- Sitting: P=0.6823, R=0.7159, F1=0.6987, support=264
- Standing: P=0.9846, R=0.2433, F1=0.3902, support=263
