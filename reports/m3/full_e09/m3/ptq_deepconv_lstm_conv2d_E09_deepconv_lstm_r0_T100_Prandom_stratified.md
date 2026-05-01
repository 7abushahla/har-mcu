# PTQ_DEEPCONV_LSTM_CONV2D_E09_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/full_e09/deepconv_lstm_conv2d_T100_Prandom_stratified_E09_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.9880
- Macro-F1: 0.9880

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.235 ms/sample
- Inference latency p95: 4.267 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/full_e09/m3/confusion_ptq_deepconv_lstm_conv2d_E09_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9742, R=1.0000, F1=0.9869, support=264
- Jogging: P=0.9962, R=0.9848, F1=0.9904, support=263
- Upstairs: P=0.9737, R=0.9811, F1=0.9774, support=264
- Downstairs: P=0.9847, R=0.9773, F1=0.9810, support=264
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=264
- Standing: P=1.0000, R=0.9848, F1=0.9923, support=263
