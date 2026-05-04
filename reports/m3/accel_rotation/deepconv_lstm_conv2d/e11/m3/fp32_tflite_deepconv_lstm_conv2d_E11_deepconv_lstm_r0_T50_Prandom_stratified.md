# FP32_TFLITE_DEEPCONV_LSTM_CONV2D_E11_DEEPCONV_LSTM_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E11_wisdm_pretrain_arduino_finetune_T50/accel_rotation/deepconv_lstm_conv2d/e11/deepconv_lstm_conv2d_T50_Prandom_stratified_E11_deepconv_lstm_r0_fp32.tflite`
- Model size: 396.43 KB
- Accuracy: 0.9224
- Macro-F1: 0.9227

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 0.307 ms/sample
- Inference latency p95: 0.329 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/accel_rotation/deepconv_lstm_conv2d/e11/m3/confusion_fp32_tflite_deepconv_lstm_conv2d_E11_deepconv_lstm_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9215, R=0.9546, F1=0.9378, support=529
- Jogging: P=0.9767, R=0.9545, F1=0.9655, support=528
- Upstairs: P=0.8108, R=0.8507, F1=0.8303, support=529
- Downstairs: P=0.8625, R=0.8314, F1=0.8467, support=528
- Sitting: P=0.9796, R=1.0000, F1=0.9897, support=528
- Standing: P=0.9901, R=0.9432, F1=0.9661, support=528
