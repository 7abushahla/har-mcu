# QAT_XTINYHAR_STUDENT_CONV2D_E04_XTINYHAR_STUDENT_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/arch_seq/xtinyhar_student_conv2d/e04/xtinyhar_student_conv2d_T100_Prandom_stratified_E04_xtinyhar_student_conv2d_r0_qat.tflite`
- Model size: 315.68 KB
- Accuracy: 0.5442
- Macro-F1: 0.5693

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 13
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONV_2D', 'FULLY_CONNECTED', 'GELU', 'MEAN', 'MUL', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.329 ms/sample
- Inference latency p95: 0.353 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/xtinyhar_student_conv2d/e04/m3/confusion_qat_xtinyhar_student_conv2d_E04_xtinyhar_student_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.5976, R=0.3826, F1=0.4665, support=264
- Jogging: P=0.9853, R=0.5095, F1=0.6717, support=263
- Upstairs: P=0.2619, R=0.5417, F1=0.3531, support=264
- Downstairs: P=0.2801, R=0.3258, F1=0.3012, support=264
- Sitting: P=0.9135, R=1.0000, F1=0.9548, support=264
- Standing: P=0.9852, R=0.5057, F1=0.6683, support=263
