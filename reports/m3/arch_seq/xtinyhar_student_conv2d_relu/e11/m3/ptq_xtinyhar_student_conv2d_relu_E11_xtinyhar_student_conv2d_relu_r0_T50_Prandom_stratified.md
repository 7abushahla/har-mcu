# PTQ_XTINYHAR_STUDENT_CONV2D_RELU_E11_XTINYHAR_STUDENT_CONV2D_RELU_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E11_wisdm_pretrain_arduino_finetune_T50/arch_seq/xtinyhar_student_conv2d_relu/e11/xtinyhar_student_conv2d_relu_T50_Prandom_stratified_E11_xtinyhar_student_conv2d_relu_r0_ptq_int8.tflite`
- Model size: 308.62 KB
- Accuracy: 0.9539
- Macro-F1: 0.9540

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 12
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 0.321 ms/sample
- Inference latency p95: 0.336 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/xtinyhar_student_conv2d_relu/e11/m3/confusion_ptq_xtinyhar_student_conv2d_relu_E11_xtinyhar_student_conv2d_relu_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9777, R=0.9924, F1=0.9850, support=529
- Jogging: P=0.9864, R=0.9621, F1=0.9741, support=528
- Upstairs: P=0.8569, R=0.8941, F1=0.8751, support=529
- Downstairs: P=0.9149, R=0.8750, F1=0.8945, support=528
- Sitting: P=0.9906, R=1.0000, F1=0.9953, support=528
- Standing: P=1.0000, R=1.0000, F1=1.0000, support=528
