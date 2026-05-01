# QAT_XTINYHAR_STUDENT_CONV2D_E11_XTINYHAR_STUDENT_CONV2D_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E11_wisdm_pretrain_arduino_finetune_T50/arch_seq/xtinyhar_student_conv2d/e11/xtinyhar_student_conv2d_T50_Prandom_stratified_E11_xtinyhar_student_conv2d_r0_qat.tflite`
- Model size: 311.93 KB
- Accuracy: 0.9681
- Macro-F1: 0.9680

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 13
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONV_2D', 'FULLY_CONNECTED', 'GELU', 'MEAN', 'MUL', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.323 ms/sample
- Inference latency p95: 0.337 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/xtinyhar_student_conv2d/e11/m3/confusion_qat_xtinyhar_student_conv2d_E11_xtinyhar_student_conv2d_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9832, R=0.9981, F1=0.9906, support=529
- Jogging: P=0.9737, R=0.9830, F1=0.9783, support=528
- Upstairs: P=0.9301, R=0.9055, F1=0.9176, support=529
- Downstairs: P=0.9294, R=0.9223, F1=0.9259, support=528
- Sitting: P=0.9925, R=1.0000, F1=0.9962, support=528
- Standing: P=0.9981, R=1.0000, F1=0.9991, support=528
