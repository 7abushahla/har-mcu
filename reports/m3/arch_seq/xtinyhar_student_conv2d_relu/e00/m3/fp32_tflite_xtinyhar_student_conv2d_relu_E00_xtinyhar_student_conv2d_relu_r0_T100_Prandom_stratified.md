# FP32_TFLITE_XTINYHAR_STUDENT_CONV2D_RELU_E00_XTINYHAR_STUDENT_CONV2D_RELU_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/arch_seq/xtinyhar_student_conv2d_relu/e00/xtinyhar_student_conv2d_relu_T100_Prandom_stratified_E00_xtinyhar_student_conv2d_relu_r0_fp32.tflite`
- Model size: 1101.16 KB
- Accuracy: 0.9365
- Macro-F1: 0.9139

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 12
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.137 ms/sample
- Inference latency p95: 0.161 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/xtinyhar_student_conv2d_relu/e00/m3/confusion_fp32_tflite_xtinyhar_student_conv2d_relu_E00_xtinyhar_student_conv2d_relu_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9550, R=0.9666, F1=0.9608, support=2723
- Jogging: P=0.9750, R=0.9796, F1=0.9773, support=2109
- Upstairs: P=0.8281, R=0.7918, F1=0.8095, support=730
- Downstairs: P=0.7911, R=0.7547, F1=0.7724, support=587
- Sitting: P=0.9870, R=0.9948, F1=0.9908, support=381
- Standing: P=0.9527, R=0.9934, F1=0.9726, support=304
