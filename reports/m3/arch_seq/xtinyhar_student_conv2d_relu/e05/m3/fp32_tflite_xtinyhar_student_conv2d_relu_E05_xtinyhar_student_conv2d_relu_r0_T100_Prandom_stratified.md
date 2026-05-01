# FP32_TFLITE_XTINYHAR_STUDENT_CONV2D_RELU_E05_XTINYHAR_STUDENT_CONV2D_RELU_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/arch_seq/xtinyhar_student_conv2d_relu/e05/xtinyhar_student_conv2d_relu_T100_Prandom_stratified_E05_xtinyhar_student_conv2d_relu_r0_fp32.tflite`
- Model size: 1101.16 KB
- Accuracy: 0.5638
- Macro-F1: 0.5882

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 12
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.140 ms/sample
- Inference latency p95: 0.157 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/xtinyhar_student_conv2d_relu/e05/m3/confusion_fp32_tflite_xtinyhar_student_conv2d_relu_E05_xtinyhar_student_conv2d_relu_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.8056, R=0.4394, F1=0.5686, support=264
- Jogging: P=0.9796, R=0.5475, F1=0.7024, support=263
- Upstairs: P=0.2654, R=0.4242, F1=0.3265, support=264
- Downstairs: P=0.3000, R=0.4659, F1=0.3650, support=264
- Sitting: P=0.8098, R=1.0000, F1=0.8949, support=264
- Standing: P=1.0000, R=0.5057, F1=0.6717, support=263
