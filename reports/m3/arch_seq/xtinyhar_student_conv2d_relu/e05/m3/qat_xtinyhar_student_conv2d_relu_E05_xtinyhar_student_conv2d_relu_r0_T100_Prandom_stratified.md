# QAT_XTINYHAR_STUDENT_CONV2D_RELU_E05_XTINYHAR_STUDENT_CONV2D_RELU_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/arch_seq/xtinyhar_student_conv2d_relu/e05/xtinyhar_student_conv2d_relu_T100_Prandom_stratified_E05_xtinyhar_student_conv2d_relu_r0_qat.tflite`
- Model size: 312.82 KB
- Accuracy: 0.5569
- Macro-F1: 0.5779

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 12
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.326 ms/sample
- Inference latency p95: 0.346 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/xtinyhar_student_conv2d_relu/e05/m3/confusion_qat_xtinyhar_student_conv2d_relu_E05_xtinyhar_student_conv2d_relu_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.6821, R=0.4470, F1=0.5400, support=264
- Jogging: P=0.9718, R=0.5247, F1=0.6815, support=263
- Upstairs: P=0.2566, R=0.4053, F1=0.3142, support=264
- Downstairs: P=0.3135, R=0.4583, F1=0.3723, support=264
- Sitting: P=0.7976, R=1.0000, F1=0.8874, support=264
- Standing: P=1.0000, R=0.5057, F1=0.6717, support=263
