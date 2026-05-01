# PTQ_TCN_INCEPTION_CONV2D_E04_TCN_INCEPTION_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/arch_seq/tcn_inception_conv2d/e04/tcn_inception_conv2d_T100_Prandom_stratified_E04_tcn_inception_conv2d_r0_ptq_int8.tflite`
- Model size: 369.92 KB
- Accuracy: 0.4956
- Macro-F1: 0.4705

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 10
- Interpreter ops: `['ADD', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'MUL', 'PAD', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 2.402 ms/sample
- Inference latency p95: 2.442 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/tcn_inception_conv2d/e04/m3/confusion_ptq_tcn_inception_conv2d_E04_tcn_inception_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.8182, R=0.0341, F1=0.0655, support=264
- Jogging: P=1.0000, R=0.5932, F1=0.7446, support=263
- Upstairs: P=0.2412, R=0.6970, F1=0.3583, support=264
- Downstairs: P=0.3619, R=0.1439, F1=0.2060, support=264
- Sitting: P=0.6423, R=1.0000, F1=0.7822, support=264
- Standing: P=0.9779, R=0.5057, F1=0.6667, support=263
