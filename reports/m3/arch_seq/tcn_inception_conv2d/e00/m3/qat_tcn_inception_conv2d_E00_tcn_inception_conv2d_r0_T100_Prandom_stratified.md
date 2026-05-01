# QAT_TCN_INCEPTION_CONV2D_E00_TCN_INCEPTION_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/arch_seq/tcn_inception_conv2d/e00/tcn_inception_conv2d_T100_Prandom_stratified_E00_tcn_inception_conv2d_r0_qat.tflite`
- Model size: 378.38 KB
- Accuracy: 0.9977
- Macro-F1: 0.9964

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 10
- Interpreter ops: `['ADD', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'MUL', 'PAD', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 2.482 ms/sample
- Inference latency p95: 2.514 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/tcn_inception_conv2d/e00/m3/confusion_qat_tcn_inception_conv2d_E00_tcn_inception_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=1.0000, R=0.9974, F1=0.9987, support=2723
- Jogging: P=0.9991, R=1.0000, F1=0.9995, support=2109
- Upstairs: P=0.9972, R=0.9904, F1=0.9938, support=730
- Downstairs: P=0.9832, R=0.9983, F1=0.9907, support=587
- Sitting: P=1.0000, R=0.9974, F1=0.9987, support=381
- Standing: P=0.9935, R=1.0000, F1=0.9967, support=304
