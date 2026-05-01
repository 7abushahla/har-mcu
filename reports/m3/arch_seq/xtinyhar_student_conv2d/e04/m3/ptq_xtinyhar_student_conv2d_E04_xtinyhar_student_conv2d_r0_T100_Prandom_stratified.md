# PTQ_XTINYHAR_STUDENT_CONV2D_E04_XTINYHAR_STUDENT_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/arch_seq/xtinyhar_student_conv2d/e04/xtinyhar_student_conv2d_T100_Prandom_stratified_E04_xtinyhar_student_conv2d_r0_ptq_int8.tflite`
- Model size: 315.21 KB
- Accuracy: 0.5095
- Macro-F1: 0.5269

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 13
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONV_2D', 'FULLY_CONNECTED', 'GELU', 'MEAN', 'MUL', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.324 ms/sample
- Inference latency p95: 0.350 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/xtinyhar_student_conv2d/e04/m3/confusion_ptq_xtinyhar_student_conv2d_E04_xtinyhar_student_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.5319, R=0.2841, F1=0.3704, support=264
- Jogging: P=0.9825, R=0.4259, F1=0.5942, support=263
- Upstairs: P=0.2427, R=0.5038, F1=0.3276, support=264
- Downstairs: P=0.2790, R=0.3371, F1=0.3053, support=264
- Sitting: P=0.8435, R=1.0000, F1=0.9151, support=264
- Standing: P=0.9048, R=0.5057, F1=0.6488, support=263
