# FP32_TFLITE_DEEPCONV_LSTM_CONV2D_E05_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/full_e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.5582
- Macro-F1: 0.5705

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 0.658 ms/sample
- Inference latency p95: 0.715 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/full_e05/m3/confusion_fp32_tflite_deepconv_lstm_conv2d_E05_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.4496, R=0.6250, F1=0.5230, support=264
- Jogging: P=1.0000, R=0.4981, F1=0.6650, support=263
- Upstairs: P=0.3430, R=0.3598, F1=0.3512, support=264
- Downstairs: P=0.2722, R=0.3598, F1=0.3100, support=264
- Sitting: P=0.9429, R=1.0000, F1=0.9706, support=264
- Standing: P=0.7472, R=0.5057, F1=0.6032, support=263
