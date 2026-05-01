# FP32_TFLITE_DEEPCONV_LSTM_CONV2D_E00_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/full_e00/deepconv_lstm_conv2d_T100_Prandom_stratified_E00_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.9798
- Macro-F1: 0.9713

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 0.648 ms/sample
- Inference latency p95: 0.680 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/full_e00/m3/confusion_fp32_tflite_deepconv_lstm_conv2d_E00_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9944, R=0.9842, F1=0.9893, support=2723
- Jogging: P=0.9952, R=0.9905, F1=0.9929, support=2109
- Upstairs: P=0.9022, R=0.9603, F1=0.9303, support=730
- Downstairs: P=0.9565, R=0.9370, F1=0.9466, support=587
- Sitting: P=0.9843, R=0.9895, F1=0.9869, support=381
- Standing: P=0.9803, R=0.9836, F1=0.9819, support=304
