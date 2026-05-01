# FP32_TFLITE_XTINYHAR_STUDENT_CONV2D_E03_XTINYHAR_STUDENT_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E03_arduino_downsample_20hz_T100/arch_seq/xtinyhar_student_conv2d/e03/xtinyhar_student_conv2d_T100_Prandom_stratified_E03_xtinyhar_student_conv2d_r0_fp32.tflite`
- Model size: 1103.78 KB
- Accuracy: 0.1669
- Macro-F1: 0.0477

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 13
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONV_2D', 'FULLY_CONNECTED', 'GELU', 'MEAN', 'MUL', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.162 ms/sample
- Inference latency p95: 0.183 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/xtinyhar_student_conv2d/e03/m3/confusion_fp32_tflite_xtinyhar_student_conv2d_E03_xtinyhar_student_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.0000, R=0.0000, F1=0.0000, support=264
- Jogging: P=0.0000, R=0.0000, F1=0.0000, support=263
- Upstairs: P=0.0000, R=0.0000, F1=0.0000, support=264
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=264
- Sitting: P=0.1669, R=1.0000, F1=0.2860, support=264
- Standing: P=0.0000, R=0.0000, F1=0.0000, support=263
