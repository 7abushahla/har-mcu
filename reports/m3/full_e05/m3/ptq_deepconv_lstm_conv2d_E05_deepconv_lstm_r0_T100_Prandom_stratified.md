# PTQ_DEEPCONV_LSTM_CONV2D_E05_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/full_e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.5809
- Macro-F1: 0.5973

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.289 ms/sample
- Inference latency p95: 4.427 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/full_e05/m3/confusion_ptq_deepconv_lstm_conv2d_E05_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.6183, R=0.5644, F1=0.5901, support=264
- Jogging: P=0.9119, R=0.5513, F1=0.6872, support=263
- Upstairs: P=0.2843, R=0.3295, F1=0.3053, support=264
- Downstairs: P=0.3243, R=0.5417, F1=0.4057, support=264
- Sitting: P=0.9167, R=1.0000, F1=0.9565, support=264
- Standing: P=0.8912, R=0.4981, F1=0.6390, support=263
