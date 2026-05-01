# FP32_TFLITE_XTINYHAR_STUDENT_CONV2D_E04_XTINYHAR_STUDENT_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/arch_seq/xtinyhar_student_conv2d/e04/xtinyhar_student_conv2d_T100_Prandom_stratified_E04_xtinyhar_student_conv2d_r0_fp32.tflite`
- Model size: 1103.78 KB
- Accuracy: 0.5221
- Macro-F1: 0.5400

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 13
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONV_2D', 'FULLY_CONNECTED', 'GELU', 'MEAN', 'MUL', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.187 ms/sample
- Inference latency p95: 0.206 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/xtinyhar_student_conv2d/e04/m3/confusion_fp32_tflite_xtinyhar_student_conv2d_E04_xtinyhar_student_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.5580, R=0.2917, F1=0.3831, support=264
- Jogging: P=0.9846, R=0.4867, F1=0.6514, support=263
- Upstairs: P=0.2500, R=0.5038, F1=0.3342, support=264
- Downstairs: P=0.2853, R=0.3447, F1=0.3122, support=264
- Sitting: P=0.8328, R=1.0000, F1=0.9088, support=264
- Standing: P=0.9110, R=0.5057, F1=0.6504, support=263
