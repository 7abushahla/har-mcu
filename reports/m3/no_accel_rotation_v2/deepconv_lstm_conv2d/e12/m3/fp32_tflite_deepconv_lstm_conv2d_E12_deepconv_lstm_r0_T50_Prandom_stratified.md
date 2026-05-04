# FP32_TFLITE_DEEPCONV_LSTM_CONV2D_E12_DEEPCONV_LSTM_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/no_accel_rotation_v2/deepconv_lstm_conv2d/e12/deepconv_lstm_conv2d_T50_Prandom_stratified_E12_deepconv_lstm_r0_fp32.tflite`
- Model size: 396.43 KB
- Accuracy: 0.8880
- Macro-F1: 0.8930

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 0.311 ms/sample
- Inference latency p95: 0.326 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/no_accel_rotation_v2/deepconv_lstm_conv2d/e12/m3/confusion_fp32_tflite_deepconv_lstm_conv2d_E12_deepconv_lstm_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9887, R=0.8242, F1=0.8990, support=529
- Jogging: P=0.9959, R=0.9280, F1=0.9608, support=528
- Upstairs: P=0.6454, R=0.9565, F1=0.7708, support=529
- Downstairs: P=0.8705, R=0.8277, F1=0.8485, support=528
- Sitting: P=0.9962, R=1.0000, F1=0.9981, support=528
- Standing: P=0.9929, R=0.7917, F1=0.8809, support=528
