# QAT_DEEPCONV_LSTM_CONV2D_E10_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E10_arduino_from_scratch/full_e10/deepconv_lstm_conv2d_T100_Prandom_stratified_E10_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.4962
- Macro-F1: 0.4752

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.254 ms/sample
- Inference latency p95: 4.298 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/full_e10/m3/confusion_qat_deepconv_lstm_conv2d_E10_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.5706, R=0.7803, F1=0.6592, support=264
- Jogging: P=1.0000, R=0.4183, F1=0.5898, support=263
- Upstairs: P=0.2182, R=0.4545, F1=0.2948, support=264
- Downstairs: P=0.4807, R=0.6136, F1=0.5391, support=264
- Sitting: P=0.0000, R=0.0000, F1=0.0000, support=264
- Standing: P=0.8348, R=0.7110, F1=0.7680, support=263
