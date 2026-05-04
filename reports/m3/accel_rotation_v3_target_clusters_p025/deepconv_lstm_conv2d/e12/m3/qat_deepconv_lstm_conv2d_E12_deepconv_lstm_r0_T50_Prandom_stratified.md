# QAT_DEEPCONV_LSTM_CONV2D_E12_DEEPCONV_LSTM_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e12/deepconv_lstm_conv2d_T50_Prandom_stratified_E12_deepconv_lstm_r0_qat.tflite`
- Model size: 108.05 KB
- Accuracy: 0.7962
- Macro-F1: 0.8012

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 2.039 ms/sample
- Inference latency p95: 2.068 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e12/m3/confusion_qat_deepconv_lstm_conv2d_E12_deepconv_lstm_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.8595, R=0.9017, F1=0.8801, support=529
- Jogging: P=0.9774, R=0.8996, F1=0.9369, support=528
- Upstairs: P=0.5719, R=0.7221, F1=0.6383, support=529
- Downstairs: P=0.6317, R=0.8314, F1=0.7179, support=528
- Sitting: P=1.0000, R=0.8485, F1=0.9180, support=528
- Standing: P=0.9528, R=0.5739, F1=0.7163, support=528
