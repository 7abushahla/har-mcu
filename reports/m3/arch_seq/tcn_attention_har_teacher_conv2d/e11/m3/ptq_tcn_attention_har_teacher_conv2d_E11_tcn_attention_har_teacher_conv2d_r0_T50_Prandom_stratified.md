# PTQ_TCN_ATTENTION_HAR_TEACHER_CONV2D_E11_TCN_ATTENTION_HAR_TEACHER_CONV2D_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E11_wisdm_pretrain_arduino_finetune_T50/arch_seq/tcn_attention_har_teacher_conv2d/e11/tcn_attention_har_teacher_conv2d_T50_Prandom_stratified_E11_tcn_attention_har_teacher_conv2d_r0_ptq_int8.tflite`
- Model size: 578.35 KB
- Accuracy: 0.9817
- Macro-F1: 0.9817

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 14
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'PAD', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 4.270 ms/sample
- Inference latency p95: 4.530 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/tcn_attention_har_teacher_conv2d/e11/m3/confusion_ptq_tcn_attention_har_teacher_conv2d_E11_tcn_attention_har_teacher_conv2d_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9925, R=0.9981, F1=0.9953, support=529
- Jogging: P=0.9943, R=0.9867, F1=0.9905, support=528
- Upstairs: P=0.9426, R=0.9622, F1=0.9523, support=529
- Downstairs: P=0.9632, R=0.9432, F1=0.9531, support=528
- Sitting: P=0.9981, R=1.0000, F1=0.9991, support=528
- Standing: P=1.0000, R=1.0000, F1=1.0000, support=528
