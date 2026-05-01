# PTQ_XTINYHAR_STUDENT_CONV2D_RELU_E00_XTINYHAR_STUDENT_CONV2D_RELU_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/arch_seq/xtinyhar_student_conv2d_relu/e00/xtinyhar_student_conv2d_relu_T100_Prandom_stratified_E00_xtinyhar_student_conv2d_relu_r0_ptq_int8.tflite`
- Model size: 312.37 KB
- Accuracy: 0.9362
- Macro-F1: 0.9133

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 12
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.323 ms/sample
- Inference latency p95: 0.348 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/xtinyhar_student_conv2d_relu/e00/m3/confusion_ptq_xtinyhar_student_conv2d_relu_E00_xtinyhar_student_conv2d_relu_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9553, R=0.9658, F1=0.9606, support=2723
- Jogging: P=0.9759, R=0.9796, F1=0.9778, support=2109
- Upstairs: P=0.8223, R=0.7986, F1=0.8103, support=730
- Downstairs: P=0.7906, R=0.7462, F1=0.7677, support=587
- Sitting: P=0.9870, R=0.9948, F1=0.9908, support=381
- Standing: P=0.9527, R=0.9934, F1=0.9726, support=304
