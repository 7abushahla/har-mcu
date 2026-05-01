# QAT_DEEPCONV_LSTM_CONV2D_E05_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/full_e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.4912
- Macro-F1: 0.4816

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.241 ms/sample
- Inference latency p95: 4.299 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/full_e05/m3/confusion_qat_deepconv_lstm_conv2d_E05_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.4718, R=0.6326, F1=0.5405, support=264
- Jogging: P=0.9143, R=0.2433, F1=0.3844, support=263
- Upstairs: P=0.3209, R=0.3258, F1=0.3233, support=264
- Downstairs: P=0.2069, R=0.2727, F1=0.2353, support=264
- Sitting: P=0.7652, R=1.0000, F1=0.8670, support=264
- Standing: P=0.6294, R=0.4715, F1=0.5391, support=263
