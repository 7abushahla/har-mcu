# FP32_TFLITE_TCN_INCEPTION_CONV2D_E00_TCN_INCEPTION_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/arch_seq/tcn_inception_conv2d/e00/tcn_inception_conv2d_T100_Prandom_stratified_E00_tcn_inception_conv2d_r0_fp32.tflite`
- Model size: 1322.99 KB
- Accuracy: 0.9965
- Macro-F1: 0.9948

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 10
- Interpreter ops: `['ADD', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'MUL', 'PAD', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 1.571 ms/sample
- Inference latency p95: 1.631 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/tcn_inception_conv2d/e00/m3/confusion_fp32_tflite_tcn_inception_conv2d_E00_tcn_inception_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9996, R=0.9963, F1=0.9980, support=2723
- Jogging: P=0.9986, R=1.0000, F1=0.9993, support=2109
- Upstairs: P=0.9931, R=0.9849, F1=0.9890, support=730
- Downstairs: P=0.9783, R=0.9966, F1=0.9873, support=587
- Sitting: P=1.0000, R=0.9974, F1=0.9987, support=381
- Standing: P=0.9935, R=1.0000, F1=0.9967, support=304
