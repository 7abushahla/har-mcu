# FP32_TFLITE_XTINYHAR_STUDENT_CONV2D_E06_XTINYHAR_STUDENT_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E06_no_norm_matched/arch_seq/xtinyhar_student_conv2d/e06/xtinyhar_student_conv2d_T100_Prandom_stratified_E06_xtinyhar_student_conv2d_r0_fp32.tflite`
- Model size: 1103.78 KB
- Accuracy: 0.1719
- Macro-F1: 0.1303

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 13
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONV_2D', 'FULLY_CONNECTED', 'GELU', 'MEAN', 'MUL', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.180 ms/sample
- Inference latency p95: 0.202 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/xtinyhar_student_conv2d/e06/m3/confusion_fp32_tflite_xtinyhar_student_conv2d_E06_xtinyhar_student_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.2296, R=0.4053, F1=0.2932, support=264
- Jogging: P=0.0930, R=0.0152, F1=0.0261, support=263
- Upstairs: P=0.1216, R=0.2045, F1=0.1525, support=264
- Downstairs: P=0.2512, R=0.4053, F1=0.3101, support=264
- Sitting: P=0.0000, R=0.0000, F1=0.0000, support=264
- Standing: P=0.0000, R=0.0000, F1=0.0000, support=263
