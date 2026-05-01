# FP32_TFLITE_DEEPCONV_LSTM_CONV2D_E09_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/full_e09/deepconv_lstm_conv2d_T100_Prandom_stratified_E09_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.9912
- Macro-F1: 0.9912

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 0.651 ms/sample
- Inference latency p95: 0.678 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/full_e09/m3/confusion_fp32_tflite_deepconv_lstm_conv2d_E09_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9888, R=1.0000, F1=0.9944, support=264
- Jogging: P=1.0000, R=0.9848, F1=0.9923, support=263
- Upstairs: P=0.9738, R=0.9848, F1=0.9793, support=264
- Downstairs: P=0.9847, R=0.9773, F1=0.9810, support=264
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=264
- Standing: P=1.0000, R=1.0000, F1=1.0000, support=263
