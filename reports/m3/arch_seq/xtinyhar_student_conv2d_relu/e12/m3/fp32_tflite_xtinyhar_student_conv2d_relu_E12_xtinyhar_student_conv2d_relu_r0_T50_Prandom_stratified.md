# FP32_TFLITE_XTINYHAR_STUDENT_CONV2D_RELU_E12_XTINYHAR_STUDENT_CONV2D_RELU_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/arch_seq/xtinyhar_student_conv2d_relu/e12/xtinyhar_student_conv2d_relu_T50_Prandom_stratified_E12_xtinyhar_student_conv2d_relu_r0_fp32.tflite`
- Model size: 1086.16 KB
- Accuracy: 0.9555
- Macro-F1: 0.9554

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 12
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.141 ms/sample
- Inference latency p95: 0.159 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/xtinyhar_student_conv2d_relu/e12/m3/confusion_fp32_tflite_xtinyhar_student_conv2d_relu_E12_xtinyhar_student_conv2d_relu_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9814, R=0.9962, F1=0.9887, support=529
- Jogging: P=0.9847, R=0.9754, F1=0.9800, support=528
- Upstairs: P=0.8863, R=0.8696, F1=0.8779, support=529
- Downstairs: P=0.8853, R=0.8920, F1=0.8887, support=528
- Sitting: P=0.9981, R=1.0000, F1=0.9991, support=528
- Standing: P=0.9962, R=1.0000, F1=0.9981, support=528
