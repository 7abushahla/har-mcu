# QAT_XTINYHAR_STUDENT_CONV2D_E00_XTINYHAR_STUDENT_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/arch_seq/xtinyhar_student_conv2d/e00/xtinyhar_student_conv2d_T100_Prandom_stratified_E00_xtinyhar_student_conv2d_r0_qat.tflite`
- Model size: 315.68 KB
- Accuracy: 0.9615
- Macro-F1: 0.9494

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 13
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONV_2D', 'FULLY_CONNECTED', 'GELU', 'MEAN', 'MUL', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.324 ms/sample
- Inference latency p95: 0.362 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/xtinyhar_student_conv2d/e00/m3/confusion_qat_xtinyhar_student_conv2d_E00_xtinyhar_student_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9665, R=0.9868, F1=0.9766, support=2723
- Jogging: P=0.9820, R=0.9844, F1=0.9832, support=2109
- Upstairs: P=0.8993, R=0.8808, F1=0.8900, support=730
- Downstairs: P=0.8965, R=0.8262, F1=0.8599, support=587
- Sitting: P=0.9948, R=0.9948, F1=0.9948, support=381
- Standing: P=0.9934, R=0.9901, F1=0.9918, support=304
