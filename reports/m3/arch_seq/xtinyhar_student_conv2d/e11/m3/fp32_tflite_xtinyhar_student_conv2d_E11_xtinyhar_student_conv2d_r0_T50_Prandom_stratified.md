# FP32_TFLITE_XTINYHAR_STUDENT_CONV2D_E11_XTINYHAR_STUDENT_CONV2D_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E11_wisdm_pretrain_arduino_finetune_T50/arch_seq/xtinyhar_student_conv2d/e11/xtinyhar_student_conv2d_T50_Prandom_stratified_E11_xtinyhar_student_conv2d_r0_fp32.tflite`
- Model size: 1088.83 KB
- Accuracy: 0.9615
- Macro-F1: 0.9615

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 13
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONV_2D', 'FULLY_CONNECTED', 'GELU', 'MEAN', 'MUL', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.193 ms/sample
- Inference latency p95: 0.211 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/xtinyhar_student_conv2d/e11/m3/confusion_fp32_tflite_xtinyhar_student_conv2d_E11_xtinyhar_student_conv2d_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9832, R=0.9943, F1=0.9887, support=529
- Jogging: P=0.9845, R=0.9640, F1=0.9742, support=528
- Upstairs: P=0.9038, R=0.8885, F1=0.8961, support=529
- Downstairs: P=0.9035, R=0.9223, F1=0.9128, support=528
- Sitting: P=0.9944, R=1.0000, F1=0.9972, support=528
- Standing: P=1.0000, R=1.0000, F1=1.0000, support=528
