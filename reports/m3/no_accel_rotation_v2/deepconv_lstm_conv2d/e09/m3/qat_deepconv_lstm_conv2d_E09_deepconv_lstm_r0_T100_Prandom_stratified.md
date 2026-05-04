# QAT_DEEPCONV_LSTM_CONV2D_E09_DEEPCONV_LSTM_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/no_accel_rotation_v2/deepconv_lstm_conv2d/e09/deepconv_lstm_conv2d_T100_Prandom_stratified_E09_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.9399
- Macro-F1: 0.9407

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 4.244 ms/sample
- Inference latency p95: 4.279 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/no_accel_rotation_v2/deepconv_lstm_conv2d/e09/m3/confusion_qat_deepconv_lstm_conv2d_E09_deepconv_lstm_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9522, R=0.9811, F1=0.9664, support=264
- Jogging: P=0.9961, R=0.9620, F1=0.9787, support=263
- Upstairs: P=0.8163, R=0.9091, F1=0.8602, support=264
- Downstairs: P=0.9080, R=0.8977, F1=0.9029, support=264
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=264
- Standing: P=0.9873, R=0.8897, F1=0.9360, support=263
