# PTQ_DEEPCONV_LSTM_CONV2D_E05_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/no_accel_rotation/deepconv_lstm_conv2d/e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.5689
- Macro-F1: 0.5959

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.245 ms/sample
- Inference latency p95: 4.273 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/no_accel_rotation/deepconv_lstm_conv2d/e05/m3/confusion_ptq_deepconv_lstm_conv2d_E05_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.8506, R=0.4962, F1=0.6268, support=264
- Jogging: P=0.9928, R=0.5247, F1=0.6866, support=263
- Upstairs: P=0.2212, R=0.2841, F1=0.2488, support=264
- Downstairs: P=0.3183, R=0.6705, F1=0.4317, support=264
- Sitting: P=0.9600, R=1.0000, F1=0.9796, support=264
- Standing: P=0.9664, R=0.4373, F1=0.6021, support=263
