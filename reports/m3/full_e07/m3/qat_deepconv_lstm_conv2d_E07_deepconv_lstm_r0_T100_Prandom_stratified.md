# QAT_DEEPCONV_LSTM_CONV2D_E07_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E07_skip_inference_norm_diag/full_e07/deepconv_lstm_conv2d_T100_Prandom_stratified_E07_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.1896
- Macro-F1: 0.0892

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.246 ms/sample
- Inference latency p95: 4.295 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/full_e07/m3/confusion_qat_deepconv_lstm_conv2d_E07_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.0000, R=0.0000, F1=0.0000, support=264
- Jogging: P=0.0000, R=0.0000, F1=0.0000, support=263
- Upstairs: P=0.1704, R=0.9962, F1=0.2911, support=264
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=264
- Sitting: P=0.9487, R=0.1402, F1=0.2442, support=264
- Standing: P=0.0000, R=0.0000, F1=0.0000, support=263
