# PTQ_XTINYHAR_STUDENT_CONV2D_RELU_E04_XTINYHAR_STUDENT_CONV2D_RELU_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/arch_seq/xtinyhar_student_conv2d_relu/e04/xtinyhar_student_conv2d_relu_T100_Prandom_stratified_E04_xtinyhar_student_conv2d_relu_r0_ptq_int8.tflite`
- Model size: 312.37 KB
- Accuracy: 0.5626
- Macro-F1: 0.5862

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 12
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.323 ms/sample
- Inference latency p95: 0.342 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/xtinyhar_student_conv2d_relu/e04/m3/confusion_ptq_xtinyhar_student_conv2d_relu_E04_xtinyhar_student_conv2d_relu_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.6689, R=0.3750, F1=0.4806, support=264
- Jogging: P=0.9720, R=0.5285, F1=0.6847, support=263
- Upstairs: P=0.2714, R=0.4318, F1=0.3333, support=264
- Downstairs: P=0.3161, R=0.5341, F1=0.3972, support=264
- Sitting: P=0.9103, R=1.0000, F1=0.9531, support=264
- Standing: P=0.9852, R=0.5057, F1=0.6683, support=263
