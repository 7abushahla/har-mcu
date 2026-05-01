# PTQ_TCN_INCEPTION_CONV2D_E12_TCN_INCEPTION_CONV2D_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/arch_seq/tcn_inception_conv2d/e12/tcn_inception_conv2d_T50_Prandom_stratified_E12_tcn_inception_conv2d_r0_ptq_int8.tflite`
- Model size: 369.92 KB
- Accuracy: 0.9868
- Macro-F1: 0.9868

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 10
- Interpreter ops: `['ADD', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'MUL', 'PAD', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 1.301 ms/sample
- Inference latency p95: 1.321 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/tcn_inception_conv2d/e12/m3/confusion_ptq_tcn_inception_conv2d_E12_tcn_inception_conv2d_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9887, R=0.9962, F1=0.9925, support=529
- Jogging: P=1.0000, R=0.9905, F1=0.9952, support=528
- Upstairs: P=0.9605, R=0.9641, F1=0.9623, support=529
- Downstairs: P=0.9715, R=0.9697, F1=0.9706, support=528
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=528
- Standing: P=1.0000, R=1.0000, F1=1.0000, support=528
