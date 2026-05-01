# PTQ_DEEPCONV_LSTM_CONV2D_E12_DEEPCONV_LSTM_CONV2D_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/arch_seq/deepconv_lstm_conv2d/e12/deepconv_lstm_conv2d_T50_Prandom_stratified_E12_deepconv_lstm_conv2d_r0_ptq_int8.tflite`
- Model size: 107.62 KB
- Accuracy: 0.8826
- Macro-F1: 0.8882

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 2.036 ms/sample
- Inference latency p95: 2.071 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/deepconv_lstm_conv2d/e12/m3/confusion_ptq_deepconv_lstm_conv2d_E12_deepconv_lstm_conv2d_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9863, R=0.8147, F1=0.8923, support=529
- Jogging: P=0.9940, R=0.9337, F1=0.9629, support=528
- Upstairs: P=0.6290, R=0.9584, F1=0.7596, support=529
- Downstairs: P=0.8773, R=0.7992, F1=0.8365, support=528
- Sitting: P=0.9962, R=1.0000, F1=0.9981, support=528
- Standing: P=0.9929, R=0.7898, F1=0.8797, support=528
