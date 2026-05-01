# FP32_TFLITE_DEEPCONV_LSTM_CONV2D_E05_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/full_e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.5847
- Macro-F1: 0.6006

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 0.650 ms/sample
- Inference latency p95: 0.704 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/full_e05/m3/confusion_fp32_tflite_deepconv_lstm_conv2d_E05_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.6040, R=0.5720, F1=0.5875, support=264
- Jogging: P=0.9152, R=0.5741, F1=0.7056, support=263
- Upstairs: P=0.2848, R=0.3333, F1=0.3072, support=264
- Downstairs: P=0.3310, R=0.5303, F1=0.4076, support=264
- Sitting: P=0.9167, R=1.0000, F1=0.9565, support=264
- Standing: P=0.8912, R=0.4981, F1=0.6390, support=263
