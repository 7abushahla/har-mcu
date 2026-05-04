# PTQ_DEEPCONV_LSTM_CONV2D_E00_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/no_accel_rotation/deepconv_lstm_conv2d/e00/deepconv_lstm_conv2d_T100_Prandom_stratified_E00_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.9797
- Macro-F1: 0.9710

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.252 ms/sample
- Inference latency p95: 4.303 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/no_accel_rotation/deepconv_lstm_conv2d/e00/m3/confusion_ptq_deepconv_lstm_conv2d_E00_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9944, R=0.9842, F1=0.9893, support=2723
- Jogging: P=0.9948, R=0.9905, F1=0.9926, support=2109
- Upstairs: P=0.9012, R=0.9616, F1=0.9304, support=730
- Downstairs: P=0.9581, R=0.9353, F1=0.9466, support=587
- Sitting: P=0.9843, R=0.9895, F1=0.9869, support=381
- Standing: P=0.9803, R=0.9803, F1=0.9803, support=304
