# QAT_DEEPCONV_LSTM_CONV2D_E04_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/full_e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.5284
- Macro-F1: 0.5415

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.253 ms/sample
- Inference latency p95: 4.332 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/full_e04/m3/confusion_qat_deepconv_lstm_conv2d_E04_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.5975, R=0.5455, F1=0.5703, support=264
- Jogging: P=1.0000, R=0.3346, F1=0.5014, support=263
- Upstairs: P=0.2521, R=0.3371, F1=0.2885, support=264
- Downstairs: P=0.2879, R=0.4886, F1=0.3624, support=264
- Sitting: P=0.9010, R=1.0000, F1=0.9479, support=264
- Standing: P=0.7673, R=0.4639, F1=0.5782, support=263
