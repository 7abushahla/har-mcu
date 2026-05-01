# QAT_TCN_INCEPTION_CONV2D_E10_TCN_INCEPTION_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E10_arduino_from_scratch/arch_seq/tcn_inception_conv2d/e10/tcn_inception_conv2d_T100_Prandom_stratified_E10_tcn_inception_conv2d_r0_qat.tflite`
- Model size: 378.38 KB
- Accuracy: 0.9956
- Macro-F1: 0.9956

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 10
- Interpreter ops: `['ADD', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'MUL', 'PAD', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 2.510 ms/sample
- Inference latency p95: 2.545 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/tcn_inception_conv2d/e10/m3/confusion_qat_tcn_inception_conv2d_E10_tcn_inception_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9925, R=1.0000, F1=0.9962, support=264
- Jogging: P=1.0000, R=0.9886, F1=0.9943, support=263
- Upstairs: P=1.0000, R=0.9848, F1=0.9924, support=264
- Downstairs: P=0.9814, R=1.0000, F1=0.9906, support=264
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=264
- Standing: P=1.0000, R=1.0000, F1=1.0000, support=263
