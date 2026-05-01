# FP32_TFLITE_DEEPCONV_LSTM_CONV2D_E12_DEEPCONV_LSTM_CONV2D_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/arch_seq/deepconv_lstm_conv2d/e12/deepconv_lstm_conv2d_T50_Prandom_stratified_E12_deepconv_lstm_conv2d_r0_fp32.tflite`
- Model size: 396.43 KB
- Accuracy: 0.8823
- Macro-F1: 0.8879

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 0.308 ms/sample
- Inference latency p95: 0.337 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/deepconv_lstm_conv2d/e12/m3/confusion_fp32_tflite_deepconv_lstm_conv2d_E12_deepconv_lstm_conv2d_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9862, R=0.8110, F1=0.8900, support=529
- Jogging: P=0.9939, R=0.9261, F1=0.9588, support=528
- Upstairs: P=0.6301, R=0.9565, F1=0.7598, support=529
- Downstairs: P=0.8730, R=0.8068, F1=0.8386, support=528
- Sitting: P=0.9962, R=1.0000, F1=0.9981, support=528
- Standing: P=0.9929, R=0.7936, F1=0.8821, support=528
