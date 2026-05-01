# FP32_TFLITE_TCN_INCEPTION_CONV2D_E05_TCN_INCEPTION_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/arch_seq/tcn_inception_conv2d/e05/tcn_inception_conv2d_T100_Prandom_stratified_E05_tcn_inception_conv2d_r0_fp32.tflite`
- Model size: 1322.99 KB
- Accuracy: 0.5398
- Macro-F1: 0.4787

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 10
- Interpreter ops: `['ADD', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'MUL', 'PAD', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 1.575 ms/sample
- Inference latency p95: 1.628 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/tcn_inception_conv2d/e05/m3/confusion_fp32_tflite_tcn_inception_conv2d_E05_tcn_inception_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.5405, R=0.0758, F1=0.1329, support=264
- Jogging: P=0.9256, R=0.7567, F1=0.8326, support=263
- Upstairs: P=0.3040, R=0.9015, F1=0.4546, support=264
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=264
- Sitting: P=0.6600, R=1.0000, F1=0.7952, support=264
- Standing: P=0.9366, R=0.5057, F1=0.6568, support=263
