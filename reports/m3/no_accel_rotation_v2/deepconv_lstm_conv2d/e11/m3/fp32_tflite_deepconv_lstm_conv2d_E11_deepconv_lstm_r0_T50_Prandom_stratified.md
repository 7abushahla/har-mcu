# FP32_TFLITE_DEEPCONV_LSTM_CONV2D_E11_DEEPCONV_LSTM_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E11_wisdm_pretrain_arduino_finetune_T50/no_accel_rotation_v2/deepconv_lstm_conv2d/e11/deepconv_lstm_conv2d_T50_Prandom_stratified_E11_deepconv_lstm_r0_fp32.tflite`
- Model size: 396.43 KB
- Accuracy: 0.9719
- Macro-F1: 0.9720

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 0.307 ms/sample
- Inference latency p95: 0.323 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/no_accel_rotation_v2/deepconv_lstm_conv2d/e11/m3/confusion_fp32_tflite_deepconv_lstm_conv2d_E11_deepconv_lstm_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9924, R=0.9811, F1=0.9867, support=529
- Jogging: P=0.9942, R=0.9792, F1=0.9866, support=528
- Upstairs: P=0.9039, R=0.9603, F1=0.9313, support=529
- Downstairs: P=0.9525, R=0.9110, F1=0.9313, support=528
- Sitting: P=0.9981, R=1.0000, F1=0.9991, support=528
- Standing: P=0.9944, R=1.0000, F1=0.9972, support=528
