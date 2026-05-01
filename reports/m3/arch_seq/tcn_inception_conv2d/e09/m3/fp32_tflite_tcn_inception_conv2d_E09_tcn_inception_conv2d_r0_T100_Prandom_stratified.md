# FP32_TFLITE_TCN_INCEPTION_CONV2D_E09_TCN_INCEPTION_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/arch_seq/tcn_inception_conv2d/e09/tcn_inception_conv2d_T100_Prandom_stratified_E09_tcn_inception_conv2d_r0_fp32.tflite`
- Model size: 1322.99 KB
- Accuracy: 0.9937
- Macro-F1: 0.9937

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 10
- Interpreter ops: `['ADD', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'MUL', 'PAD', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 1.561 ms/sample
- Inference latency p95: 1.582 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/tcn_inception_conv2d/e09/m3/confusion_fp32_tflite_tcn_inception_conv2d_E09_tcn_inception_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9962, R=1.0000, F1=0.9981, support=264
- Jogging: P=0.9962, R=0.9886, F1=0.9924, support=263
- Upstairs: P=1.0000, R=0.9735, F1=0.9866, support=264
- Downstairs: P=0.9706, R=1.0000, F1=0.9851, support=264
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=264
- Standing: P=1.0000, R=1.0000, F1=1.0000, support=263
