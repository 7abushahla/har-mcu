# FP32_TFLITE_DEEPCONV_LSTM_CONV2D_E11_DEEPCONV_LSTM_CONV2D_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E11_wisdm_pretrain_arduino_finetune_T50/arch_seq/deepconv_lstm_conv2d/e11/deepconv_lstm_conv2d_T50_Prandom_stratified_E11_deepconv_lstm_conv2d_r0_fp32.tflite`
- Model size: 396.43 KB
- Accuracy: 0.9653
- Macro-F1: 0.9655

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Inference latency median: 0.312 ms/sample
- Inference latency p95: 0.328 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/deepconv_lstm_conv2d/e11/m3/confusion_fp32_tflite_deepconv_lstm_conv2d_E11_deepconv_lstm_conv2d_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9904, R=0.9716, F1=0.9809, support=529
- Jogging: P=0.9905, R=0.9830, F1=0.9867, support=528
- Upstairs: P=0.8836, R=0.9471, F1=0.9142, support=529
- Downstairs: P=0.9368, R=0.8977, F1=0.9168, support=528
- Sitting: P=0.9962, R=1.0000, F1=0.9981, support=528
- Standing: P=1.0000, R=0.9924, F1=0.9962, support=528
