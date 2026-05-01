# QAT_TCN_INCEPTION_CONV2D_E05_TCN_INCEPTION_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/arch_seq/tcn_inception_conv2d/e05/tcn_inception_conv2d_T100_Prandom_stratified_E05_tcn_inception_conv2d_r0_qat.tflite`
- Model size: 378.38 KB
- Accuracy: 0.5171
- Macro-F1: 0.4996

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 10
- Interpreter ops: `['ADD', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'MUL', 'PAD', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 2.514 ms/sample
- Inference latency p95: 2.541 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/tcn_inception_conv2d/e05/m3/confusion_qat_tcn_inception_conv2d_E05_tcn_inception_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.5556, R=0.0189, F1=0.0366, support=264
- Jogging: P=0.9661, R=0.6502, F1=0.7773, support=263
- Upstairs: P=0.2683, R=0.7765, F1=0.3988, support=264
- Downstairs: P=0.1980, R=0.1515, F1=0.1717, support=264
- Sitting: P=0.8980, R=1.0000, F1=0.9462, support=264
- Standing: P=0.9779, R=0.5057, F1=0.6667, support=263
