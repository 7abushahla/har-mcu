# FP32_TFLITE_TCN_ATTENTION_HAR_TEACHER_CONV2D_E05_TCN_ATTENTION_HAR_TEACHER_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/arch_seq/tcn_attention_har_teacher_conv2d/e05/tcn_attention_har_teacher_conv2d_T100_Prandom_stratified_E05_tcn_attention_har_teacher_conv2d_r0_fp32.tflite`
- Model size: 1883.36 KB
- Accuracy: 0.5936
- Macro-F1: 0.5973

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 14
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'PAD', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 2.067 ms/sample
- Inference latency p95: 2.125 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/tcn_attention_har_teacher_conv2d/e05/m3/confusion_fp32_tflite_tcn_attention_har_teacher_conv2d_E05_tcn_attention_har_teacher_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.6774, R=0.3182, F1=0.4330, support=264
- Jogging: P=0.8609, R=0.8707, F1=0.8658, support=263
- Upstairs: P=0.3357, R=0.7045, F1=0.4548, support=264
- Downstairs: P=0.1845, R=0.1629, F1=0.1730, support=264
- Sitting: P=0.9851, R=1.0000, F1=0.9925, support=264
- Standing: P=0.9708, R=0.5057, F1=0.6650, support=263
