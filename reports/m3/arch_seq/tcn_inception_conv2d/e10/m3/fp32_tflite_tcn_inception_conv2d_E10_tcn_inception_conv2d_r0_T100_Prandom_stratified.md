# FP32_TFLITE_TCN_INCEPTION_CONV2D_E10_TCN_INCEPTION_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E10_arduino_from_scratch/arch_seq/tcn_inception_conv2d/e10/tcn_inception_conv2d_T100_Prandom_stratified_E10_tcn_inception_conv2d_r0_fp32.tflite`
- Model size: 1322.99 KB
- Accuracy: 0.9924
- Macro-F1: 0.9924

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 10
- Interpreter ops: `['ADD', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'MUL', 'PAD', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 1.583 ms/sample
- Inference latency p95: 1.641 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/tcn_inception_conv2d/e10/m3/confusion_fp32_tflite_tcn_inception_conv2d_E10_tcn_inception_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9851, R=1.0000, F1=0.9925, support=264
- Jogging: P=1.0000, R=0.9886, F1=0.9943, support=263
- Upstairs: P=0.9961, R=0.9697, F1=0.9827, support=264
- Downstairs: P=0.9813, R=0.9962, F1=0.9887, support=264
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=264
- Standing: P=0.9925, R=1.0000, F1=0.9962, support=263
