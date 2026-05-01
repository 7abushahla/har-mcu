# PTQ_DEEPCONV_LSTM_CONV2D_E05_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/full_e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.5499
- Macro-F1: 0.5626

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.251 ms/sample
- Inference latency p95: 4.346 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/full_e05/m3/confusion_ptq_deepconv_lstm_conv2d_E05_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.4427, R=0.6288, F1=0.5196, support=264
- Jogging: P=1.0000, R=0.4563, F1=0.6266, support=263
- Upstairs: P=0.3382, R=0.3523, F1=0.3451, support=264
- Downstairs: P=0.2632, R=0.3598, F1=0.3040, support=264
- Sitting: P=0.9531, R=1.0000, F1=0.9760, support=264
- Standing: P=0.7586, R=0.5019, F1=0.6041, support=263
