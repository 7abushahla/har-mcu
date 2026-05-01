# QAT_TCN_INCEPTION_CONV2D_E04_TCN_INCEPTION_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/arch_seq/tcn_inception_conv2d/e04/tcn_inception_conv2d_T100_Prandom_stratified_E04_tcn_inception_conv2d_r0_qat.tflite`
- Model size: 378.38 KB
- Accuracy: 0.4987
- Macro-F1: 0.4820

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 10
- Interpreter ops: `['ADD', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'MUL', 'PAD', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 2.486 ms/sample
- Inference latency p95: 2.517 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/tcn_inception_conv2d/e04/m3/confusion_qat_tcn_inception_conv2d_E04_tcn_inception_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.7222, R=0.0492, F1=0.0922, support=264
- Jogging: P=1.0000, R=0.6084, F1=0.7565, support=263
- Upstairs: P=0.2303, R=0.6212, F1=0.3361, support=264
- Downstairs: P=0.4365, R=0.2083, F1=0.2821, support=264
- Sitting: P=0.6197, R=1.0000, F1=0.7652, support=264
- Standing: P=0.9500, R=0.5057, F1=0.6600, support=263
