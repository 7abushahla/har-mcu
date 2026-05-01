# PTQ_DEEPCONV_LSTM_CONV2D_E06_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E06_no_norm_matched/full_e06/deepconv_lstm_conv2d_T100_Prandom_stratified_E06_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.1675
- Macro-F1: 0.0519

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.270 ms/sample
- Inference latency p95: 4.385 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/full_e06/m3/confusion_ptq_deepconv_lstm_conv2d_E06_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.0000, R=0.0000, F1=0.0000, support=264
- Jogging: P=0.0000, R=0.0000, F1=0.0000, support=263
- Upstairs: P=0.0149, R=0.0038, F1=0.0060, support=264
- Downstairs: P=0.0833, R=0.0038, F1=0.0072, support=264
- Sitting: P=0.0000, R=0.0000, F1=0.0000, support=264
- Standing: P=0.1751, R=1.0000, F1=0.2980, support=263
