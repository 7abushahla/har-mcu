# QAT_DEEPCONV_LSTM_CONV2D_E00_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/accel_rotation/deepconv_lstm_conv2d/e00/deepconv_lstm_conv2d_T100_Prandom_stratified_E00_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.4320
- Macro-F1: 0.3073

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.251 ms/sample
- Inference latency p95: 4.305 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/accel_rotation/deepconv_lstm_conv2d/e00/m3/confusion_qat_deepconv_lstm_conv2d_E00_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.7738, R=0.3342, F1=0.4668, support=2723
- Jogging: P=0.9749, R=0.5519, F1=0.7048, support=2109
- Upstairs: P=0.1943, R=0.6575, F1=0.2999, support=730
- Downstairs: P=0.1945, R=0.6559, F1=0.3001, support=587
- Sitting: P=0.9000, R=0.0236, F1=0.0460, support=381
- Standing: P=1.0000, R=0.0132, F1=0.0260, support=304
