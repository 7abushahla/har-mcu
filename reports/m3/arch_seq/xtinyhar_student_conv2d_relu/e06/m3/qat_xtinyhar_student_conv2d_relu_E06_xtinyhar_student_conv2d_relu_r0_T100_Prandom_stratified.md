# QAT_XTINYHAR_STUDENT_CONV2D_RELU_E06_XTINYHAR_STUDENT_CONV2D_RELU_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E06_no_norm_matched/arch_seq/xtinyhar_student_conv2d_relu/e06/xtinyhar_student_conv2d_relu_T100_Prandom_stratified_E06_xtinyhar_student_conv2d_relu_r0_qat.tflite`
- Model size: 312.82 KB
- Accuracy: 0.1612
- Macro-F1: 0.0674

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 12
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.327 ms/sample
- Inference latency p95: 0.381 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/xtinyhar_student_conv2d_relu/e06/m3/confusion_qat_xtinyhar_student_conv2d_relu_E06_xtinyhar_student_conv2d_relu_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.1771, R=0.9015, F1=0.2960, support=264
- Jogging: P=0.0120, R=0.0076, F1=0.0093, support=263
- Upstairs: P=0.1385, R=0.0341, F1=0.0547, support=264
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=264
- Sitting: P=1.0000, R=0.0227, F1=0.0444, support=264
- Standing: P=0.0000, R=0.0000, F1=0.0000, support=263
