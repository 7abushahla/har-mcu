# FP32_TFLITE_XTINYHAR_STUDENT_CONV2D_RELU_E10_XTINYHAR_STUDENT_CONV2D_RELU_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E10_arduino_from_scratch/arch_seq/xtinyhar_student_conv2d_relu/e10/xtinyhar_student_conv2d_relu_T100_Prandom_stratified_E10_xtinyhar_student_conv2d_relu_r0_fp32.tflite`
- Model size: 1101.16 KB
- Accuracy: 0.9735
- Macro-F1: 0.9734

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 12
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.144 ms/sample
- Inference latency p95: 0.162 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/xtinyhar_student_conv2d_relu/e10/m3/confusion_fp32_tflite_xtinyhar_student_conv2d_relu_E10_xtinyhar_student_conv2d_relu_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9888, R=1.0000, F1=0.9944, support=264
- Jogging: P=0.9810, R=0.9810, F1=0.9810, support=263
- Upstairs: P=0.9488, R=0.9129, F1=0.9305, support=264
- Downstairs: P=0.9225, R=0.9470, F1=0.9346, support=264
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=264
- Standing: P=1.0000, R=1.0000, F1=1.0000, support=263
