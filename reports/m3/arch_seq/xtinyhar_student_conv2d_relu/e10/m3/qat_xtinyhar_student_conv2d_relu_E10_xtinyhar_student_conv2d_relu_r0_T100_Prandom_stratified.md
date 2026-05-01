# QAT_XTINYHAR_STUDENT_CONV2D_RELU_E10_XTINYHAR_STUDENT_CONV2D_RELU_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E10_arduino_from_scratch/arch_seq/xtinyhar_student_conv2d_relu/e10/xtinyhar_student_conv2d_relu_T100_Prandom_stratified_E10_xtinyhar_student_conv2d_relu_r0_qat.tflite`
- Model size: 312.82 KB
- Accuracy: 0.9804
- Macro-F1: 0.9804

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 12
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.324 ms/sample
- Inference latency p95: 0.356 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/xtinyhar_student_conv2d_relu/e10/m3/confusion_qat_xtinyhar_student_conv2d_relu_E10_xtinyhar_student_conv2d_relu_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9851, R=1.0000, F1=0.9925, support=264
- Jogging: P=0.9848, R=0.9886, F1=0.9867, support=263
- Upstairs: P=0.9538, R=0.9394, F1=0.9466, support=264
- Downstairs: P=0.9582, R=0.9545, F1=0.9564, support=264
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=264
- Standing: P=1.0000, R=1.0000, F1=1.0000, support=263
