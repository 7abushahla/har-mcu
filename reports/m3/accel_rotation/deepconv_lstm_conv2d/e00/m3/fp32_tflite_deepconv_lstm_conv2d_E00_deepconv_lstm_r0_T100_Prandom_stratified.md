# FP32_TFLITE_DEEPCONV_LSTM_CONV2D_E00_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/accel_rotation/deepconv_lstm_conv2d/e00/deepconv_lstm_conv2d_T100_Prandom_stratified_E00_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.9444
- Macro-F1: 0.8890

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 0.646 ms/sample
- Inference latency p95: 0.672 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/accel_rotation/deepconv_lstm_conv2d/e00/m3/confusion_fp32_tflite_deepconv_lstm_conv2d_E00_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9893, R=0.9864, F1=0.9879, support=2723
- Jogging: P=0.9947, R=0.9782, F1=0.9864, support=2109
- Upstairs: P=0.7085, R=0.9658, F1=0.8174, support=730
- Downstairs: P=0.9457, R=0.8603, F1=0.9010, support=587
- Sitting: P=0.9965, R=0.7454, F1=0.8529, support=381
- Standing: P=0.9134, R=0.6941, F1=0.7888, support=304
