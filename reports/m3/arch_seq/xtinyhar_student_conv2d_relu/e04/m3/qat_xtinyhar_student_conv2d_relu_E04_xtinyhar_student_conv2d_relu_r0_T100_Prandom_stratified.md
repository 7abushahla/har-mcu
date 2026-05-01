# QAT_XTINYHAR_STUDENT_CONV2D_RELU_E04_XTINYHAR_STUDENT_CONV2D_RELU_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/arch_seq/xtinyhar_student_conv2d_relu/e04/xtinyhar_student_conv2d_relu_T100_Prandom_stratified_E04_xtinyhar_student_conv2d_relu_r0_qat.tflite`
- Model size: 312.82 KB
- Accuracy: 0.5537
- Macro-F1: 0.5791

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 12
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.325 ms/sample
- Inference latency p95: 0.348 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/xtinyhar_student_conv2d_relu/e04/m3/confusion_qat_xtinyhar_student_conv2d_relu_E04_xtinyhar_student_conv2d_relu_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.6950, R=0.3712, F1=0.4840, support=264
- Jogging: P=0.9790, R=0.5323, F1=0.6897, support=263
- Upstairs: P=0.2500, R=0.4356, F1=0.3177, support=264
- Downstairs: P=0.3119, R=0.4773, F1=0.3772, support=264
- Sitting: P=0.8859, R=1.0000, F1=0.9395, support=264
- Standing: P=0.9779, R=0.5057, F1=0.6667, support=263
