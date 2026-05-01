# PTQ_DEEPCONV_LSTM_CONV2D_E10_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E10_arduino_from_scratch/full_e10/deepconv_lstm_conv2d_T100_Prandom_stratified_E10_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.9532
- Macro-F1: 0.9540

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.253 ms/sample
- Inference latency p95: 4.329 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/full_e10/m3/confusion_ptq_deepconv_lstm_conv2d_E10_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9881, R=0.9470, F1=0.9671, support=264
- Jogging: P=0.9884, R=0.9696, F1=0.9789, support=263
- Upstairs: P=0.7988, R=0.9773, F1=0.8790, support=264
- Downstairs: P=0.9909, R=0.8258, F1=0.9008, support=264
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=264
- Standing: P=0.9962, R=1.0000, F1=0.9981, support=263
