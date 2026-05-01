# PTQ_TCN_INCEPTION_CONV2D_E05_TCN_INCEPTION_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/arch_seq/tcn_inception_conv2d/e05/tcn_inception_conv2d_T100_Prandom_stratified_E05_tcn_inception_conv2d_r0_ptq_int8.tflite`
- Model size: 369.92 KB
- Accuracy: 0.5354
- Macro-F1: 0.4802

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 10
- Interpreter ops: `['ADD', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'MUL', 'PAD', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 2.414 ms/sample
- Inference latency p95: 2.440 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/tcn_inception_conv2d/e05/m3/confusion_ptq_tcn_inception_conv2d_E05_tcn_inception_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.5938, R=0.0720, F1=0.1284, support=264
- Jogging: P=0.9630, R=0.6920, F1=0.8053, support=263
- Upstairs: P=0.3019, R=0.9205, F1=0.4546, support=264
- Downstairs: P=0.5000, R=0.0227, F1=0.0435, support=264
- Sitting: P=0.6567, R=1.0000, F1=0.7928, support=264
- Standing: P=0.9366, R=0.5057, F1=0.6568, support=263
