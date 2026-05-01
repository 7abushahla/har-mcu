# PTQ_XTINYHAR_STUDENT_CONV2D_E12_XTINYHAR_STUDENT_CONV2D_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/arch_seq/xtinyhar_student_conv2d/e12/xtinyhar_student_conv2d_T50_Prandom_stratified_E12_xtinyhar_student_conv2d_r0_ptq_int8.tflite`
- Model size: 311.46 KB
- Accuracy: 0.9590
- Macro-F1: 0.9589

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 13
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONV_2D', 'FULLY_CONNECTED', 'GELU', 'MEAN', 'MUL', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.319 ms/sample
- Inference latency p95: 0.340 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/xtinyhar_student_conv2d/e12/m3/confusion_ptq_xtinyhar_student_conv2d_E12_xtinyhar_student_conv2d_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9795, R=0.9943, F1=0.9869, support=529
- Jogging: P=0.9808, R=0.9697, F1=0.9752, support=528
- Upstairs: P=0.9069, R=0.8658, F1=0.8859, support=529
- Downstairs: P=0.8905, R=0.9242, F1=0.9071, support=528
- Sitting: P=0.9981, R=1.0000, F1=0.9991, support=528
- Standing: P=0.9981, R=1.0000, F1=0.9991, support=528
