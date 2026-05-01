# FP32_TFLITE_XTINYHAR_STUDENT_CONV2D_E09_XTINYHAR_STUDENT_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/arch_seq/xtinyhar_student_conv2d/e09/xtinyhar_student_conv2d_T100_Prandom_stratified_E09_xtinyhar_student_conv2d_r0_fp32.tflite`
- Model size: 1103.83 KB
- Accuracy: 0.9791
- Macro-F1: 0.9791

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 13
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONV_2D', 'FULLY_CONNECTED', 'GELU', 'MEAN', 'MUL', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.187 ms/sample
- Inference latency p95: 0.207 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/xtinyhar_student_conv2d/e09/m3/confusion_fp32_tflite_xtinyhar_student_conv2d_E09_xtinyhar_student_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9925, R=1.0000, F1=0.9962, support=264
- Jogging: P=0.9923, R=0.9848, F1=0.9885, support=263
- Upstairs: P=0.9368, R=0.9545, F1=0.9456, support=264
- Downstairs: P=0.9611, R=0.9356, F1=0.9482, support=264
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=264
- Standing: P=0.9925, R=1.0000, F1=0.9962, support=263
