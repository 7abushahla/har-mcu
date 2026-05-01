# QAT_DEEPCONV_LSTM_CONV2D_E00_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/full_e00/deepconv_lstm_conv2d_T100_Prandom_stratified_E00_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.8187
- Macro-F1: 0.7736

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.251 ms/sample
- Inference latency p95: 4.348 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/full_e00/m3/confusion_qat_deepconv_lstm_conv2d_E00_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9384, R=0.8784, F1=0.9074, support=2723
- Jogging: P=0.9826, R=0.7781, F1=0.8685, support=2109
- Upstairs: P=0.5174, R=0.7726, F1=0.6198, support=730
- Downstairs: P=0.5057, R=0.6082, F1=0.5522, support=587
- Sitting: P=0.8326, R=0.9790, F1=0.8999, support=381
- Standing: P=0.7224, R=0.8816, F1=0.7941, support=304
