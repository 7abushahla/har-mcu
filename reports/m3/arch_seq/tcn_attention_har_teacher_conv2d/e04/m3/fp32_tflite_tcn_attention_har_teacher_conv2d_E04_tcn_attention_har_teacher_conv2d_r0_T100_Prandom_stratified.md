# FP32_TFLITE_TCN_ATTENTION_HAR_TEACHER_CONV2D_E04_TCN_ATTENTION_HAR_TEACHER_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/arch_seq/tcn_attention_har_teacher_conv2d/e04/tcn_attention_har_teacher_conv2d_T100_Prandom_stratified_E04_tcn_attention_har_teacher_conv2d_r0_fp32.tflite`
- Model size: 1883.36 KB
- Accuracy: 0.5120
- Macro-F1: 0.4689

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 14
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'PAD', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 2.059 ms/sample
- Inference latency p95: 2.112 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/tcn_attention_har_teacher_conv2d/e04/m3/confusion_fp32_tflite_tcn_attention_har_teacher_conv2d_E04_tcn_attention_har_teacher_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.4634, R=0.1439, F1=0.2197, support=264
- Jogging: P=0.7552, R=0.9620, F1=0.8462, support=263
- Upstairs: P=0.2323, R=0.3864, F1=0.2902, support=264
- Downstairs: P=0.3279, R=0.0758, F1=0.1231, support=264
- Sitting: P=0.4972, R=1.0000, F1=0.6642, support=264
- Standing: P=0.9925, R=0.5057, F1=0.6700, support=263
