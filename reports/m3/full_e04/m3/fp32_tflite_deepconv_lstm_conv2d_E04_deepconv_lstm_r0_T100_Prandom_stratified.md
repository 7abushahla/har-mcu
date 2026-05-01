# FP32_TFLITE_DEEPCONV_LSTM_CONV2D_E04_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/full_e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.5417
- Macro-F1: 0.5636

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 0.649 ms/sample
- Inference latency p95: 0.676 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/full_e04/m3/confusion_fp32_tflite_deepconv_lstm_conv2d_E04_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.6044, R=0.5152, F1=0.5562, support=264
- Jogging: P=1.0000, R=0.4221, F1=0.5936, support=263
- Upstairs: P=0.2277, R=0.2992, F1=0.2586, support=264
- Downstairs: P=0.3018, R=0.5682, F1=0.3942, support=264
- Sitting: P=0.9496, R=1.0000, F1=0.9742, support=264
- Standing: P=0.9435, R=0.4449, F1=0.6047, support=263
