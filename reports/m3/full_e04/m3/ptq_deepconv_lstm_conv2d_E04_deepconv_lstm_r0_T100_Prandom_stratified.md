# PTQ_DEEPCONV_LSTM_CONV2D_E04_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/full_e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.5550
- Macro-F1: 0.5820

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.249 ms/sample
- Inference latency p95: 4.353 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/full_e04/m3/confusion_ptq_deepconv_lstm_conv2d_E04_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.8467, R=0.4811, F1=0.6135, support=264
- Jogging: P=1.0000, R=0.5019, F1=0.6684, support=263
- Upstairs: P=0.2210, R=0.2955, F1=0.2528, support=264
- Downstairs: P=0.3090, R=0.6742, F1=0.4238, support=264
- Sitting: P=0.9851, R=1.0000, F1=0.9925, support=264
- Standing: P=0.9612, R=0.3764, F1=0.5410, support=263
