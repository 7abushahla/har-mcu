# FP32_TFLITE_TCN_INCEPTION_CONV2D_E04_TCN_INCEPTION_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/arch_seq/tcn_inception_conv2d/e04/tcn_inception_conv2d_T100_Prandom_stratified_E04_tcn_inception_conv2d_r0_fp32.tflite`
- Model size: 1322.99 KB
- Accuracy: 0.5019
- Macro-F1: 0.4726

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 10
- Interpreter ops: `['ADD', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'MUL', 'PAD', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 1.590 ms/sample
- Inference latency p95: 1.629 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/tcn_inception_conv2d/e04/m3/confusion_fp32_tflite_tcn_inception_conv2d_E04_tcn_inception_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.6364, R=0.0265, F1=0.0509, support=264
- Jogging: P=0.9767, R=0.6388, F1=0.7724, support=263
- Upstairs: P=0.2470, R=0.7045, F1=0.3658, support=264
- Downstairs: P=0.3636, R=0.1364, F1=0.1983, support=264
- Sitting: P=0.6455, R=1.0000, F1=0.7845, support=264
- Standing: P=0.9638, R=0.5057, F1=0.6633, support=263
