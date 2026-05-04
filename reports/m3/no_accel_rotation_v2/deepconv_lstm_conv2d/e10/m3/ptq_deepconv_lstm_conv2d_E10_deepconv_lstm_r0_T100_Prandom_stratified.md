# PTQ_DEEPCONV_LSTM_CONV2D_E10_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E10_arduino_from_scratch/no_accel_rotation_v2/deepconv_lstm_conv2d/e10/deepconv_lstm_conv2d_T100_Prandom_stratified_E10_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.9406
- Macro-F1: 0.9403

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.243 ms/sample
- Inference latency p95: 4.290 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/no_accel_rotation_v2/deepconv_lstm_conv2d/e10/m3/confusion_ptq_deepconv_lstm_conv2d_E10_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9684, R=0.9280, F1=0.9478, support=264
- Jogging: P=0.9885, R=0.9848, F1=0.9867, support=263
- Upstairs: P=0.7877, R=0.9697, F1=0.8693, support=264
- Downstairs: P=0.9901, R=0.7614, F1=0.8608, support=264
- Sitting: P=0.9670, R=1.0000, F1=0.9832, support=264
- Standing: P=0.9887, R=1.0000, F1=0.9943, support=263
