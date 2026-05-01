# QAT_DEEPCONV_LSTM_CONV2D_E05_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/full_e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.5310
- Macro-F1: 0.5427

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.315 ms/sample
- Inference latency p95: 4.436 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/full_e05/m3/confusion_qat_deepconv_lstm_conv2d_E05_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.5352, R=0.5758, F1=0.5547, support=264
- Jogging: P=1.0000, R=0.3460, F1=0.5141, support=263
- Upstairs: P=0.2660, R=0.3144, F1=0.2882, support=264
- Downstairs: P=0.2719, R=0.4470, F1=0.3381, support=264
- Sitting: P=0.9041, R=1.0000, F1=0.9496, support=264
- Standing: P=0.7811, R=0.5019, F1=0.6111, support=263
