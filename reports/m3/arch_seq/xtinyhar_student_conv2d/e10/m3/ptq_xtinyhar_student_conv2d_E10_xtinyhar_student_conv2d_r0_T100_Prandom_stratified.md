# PTQ_XTINYHAR_STUDENT_CONV2D_E10_XTINYHAR_STUDENT_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E10_arduino_from_scratch/arch_seq/xtinyhar_student_conv2d/e10/xtinyhar_student_conv2d_T100_Prandom_stratified_E10_xtinyhar_student_conv2d_r0_ptq_int8.tflite`
- Model size: 315.21 KB
- Accuracy: 0.9779
- Macro-F1: 0.9778

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 13
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONV_2D', 'FULLY_CONNECTED', 'GELU', 'MEAN', 'MUL', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.320 ms/sample
- Inference latency p95: 0.343 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/xtinyhar_student_conv2d/e10/m3/confusion_ptq_xtinyhar_student_conv2d_E10_xtinyhar_student_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9600, R=1.0000, F1=0.9796, support=264
- Jogging: P=0.9844, R=0.9620, F1=0.9731, support=263
- Upstairs: P=0.9686, R=0.9356, F1=0.9518, support=264
- Downstairs: P=0.9552, R=0.9697, F1=0.9624, support=264
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=264
- Standing: P=1.0000, R=1.0000, F1=1.0000, support=263
