# QAT_XTINYHAR_STUDENT_CONV2D_E05_XTINYHAR_STUDENT_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/arch_seq/xtinyhar_student_conv2d/e05/xtinyhar_student_conv2d_T100_Prandom_stratified_E05_xtinyhar_student_conv2d_r0_qat.tflite`
- Model size: 315.68 KB
- Accuracy: 0.5303
- Macro-F1: 0.5517

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 13
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONV_2D', 'FULLY_CONNECTED', 'GELU', 'MEAN', 'MUL', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.327 ms/sample
- Inference latency p95: 0.350 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/xtinyhar_student_conv2d/e05/m3/confusion_qat_xtinyhar_student_conv2d_E05_xtinyhar_student_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.6125, R=0.3712, F1=0.4623, support=264
- Jogging: P=0.9565, R=0.5019, F1=0.6584, support=263
- Upstairs: P=0.2362, R=0.4545, F1=0.3109, support=264
- Downstairs: P=0.2939, R=0.3485, F1=0.3189, support=264
- Sitting: P=0.8123, R=1.0000, F1=0.8964, support=264
- Standing: P=0.9638, R=0.5057, F1=0.6633, support=263
