# QAT_XTINYHAR_STUDENT_CONV2D_RELU_E00_XTINYHAR_STUDENT_CONV2D_RELU_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/arch_seq/xtinyhar_student_conv2d_relu/e00/xtinyhar_student_conv2d_relu_T100_Prandom_stratified_E00_xtinyhar_student_conv2d_relu_r0_qat.tflite`
- Model size: 312.82 KB
- Accuracy: 0.9511
- Macro-F1: 0.9345

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 12
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.323 ms/sample
- Inference latency p95: 0.340 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/xtinyhar_student_conv2d_relu/e00/m3/confusion_qat_xtinyhar_student_conv2d_relu_E00_xtinyhar_student_conv2d_relu_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9617, R=0.9787, F1=0.9701, support=2723
- Jogging: P=0.9819, R=0.9801, F1=0.9810, support=2109
- Upstairs: P=0.8525, R=0.8548, F1=0.8536, support=730
- Downstairs: P=0.8701, R=0.7871, F1=0.8265, support=587
- Sitting: P=0.9896, R=0.9948, F1=0.9921, support=381
- Standing: P=0.9712, R=0.9967, F1=0.9838, support=304
