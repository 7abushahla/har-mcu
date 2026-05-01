# QAT_XTINYHAR_STUDENT_CONV2D_RELU_E11_XTINYHAR_STUDENT_CONV2D_RELU_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E11_wisdm_pretrain_arduino_finetune_T50/arch_seq/xtinyhar_student_conv2d_relu/e11/xtinyhar_student_conv2d_relu_T50_Prandom_stratified_E11_xtinyhar_student_conv2d_relu_r0_qat.tflite`
- Model size: 309.07 KB
- Accuracy: 0.9565
- Macro-F1: 0.9563

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 12
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.322 ms/sample
- Inference latency p95: 0.341 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/xtinyhar_student_conv2d_relu/e11/m3/confusion_qat_xtinyhar_student_conv2d_relu_E11_xtinyhar_student_conv2d_relu_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9814, R=0.9962, F1=0.9887, support=529
- Jogging: P=0.9774, R=0.9830, F1=0.9802, support=528
- Upstairs: P=0.8706, R=0.8904, F1=0.8804, support=529
- Downstairs: P=0.9162, R=0.8693, F1=0.8921, support=528
- Sitting: P=0.9925, R=1.0000, F1=0.9962, support=528
- Standing: P=1.0000, R=1.0000, F1=1.0000, support=528
