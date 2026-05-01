# PTQ_XTINYHAR_STUDENT_CONV2D_RELU_E05_XTINYHAR_STUDENT_CONV2D_RELU_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/arch_seq/xtinyhar_student_conv2d_relu/e05/xtinyhar_student_conv2d_relu_T100_Prandom_stratified_E05_xtinyhar_student_conv2d_relu_r0_ptq_int8.tflite`
- Model size: 312.37 KB
- Accuracy: 0.5569
- Macro-F1: 0.5817

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 12
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.324 ms/sample
- Inference latency p95: 0.346 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/xtinyhar_student_conv2d_relu/e05/m3/confusion_ptq_xtinyhar_student_conv2d_relu_E05_xtinyhar_student_conv2d_relu_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.7871, R=0.4621, F1=0.5823, support=264
- Jogging: P=0.9778, R=0.5019, F1=0.6633, support=263
- Upstairs: P=0.2541, R=0.4129, F1=0.3146, support=264
- Downstairs: P=0.2988, R=0.4583, F1=0.3617, support=264
- Sitting: P=0.8123, R=1.0000, F1=0.8964, support=264
- Standing: P=1.0000, R=0.5057, F1=0.6717, support=263
