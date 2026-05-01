# QAT_TCN_ATTENTION_HAR_TEACHER_CONV2D_E09_TCN_ATTENTION_HAR_TEACHER_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/arch_seq/tcn_attention_har_teacher_conv2d/e09/tcn_attention_har_teacher_conv2d_T100_Prandom_stratified_E09_tcn_attention_har_teacher_conv2d_r0_qat.tflite`
- Model size: 585.59 KB
- Accuracy: 0.9956
- Macro-F1: 0.9956

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 14
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'PAD', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 8.169 ms/sample
- Inference latency p95: 8.574 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/tcn_attention_har_teacher_conv2d/e09/m3/confusion_qat_tcn_attention_har_teacher_conv2d_E09_tcn_attention_har_teacher_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9962, R=1.0000, F1=0.9981, support=264
- Jogging: P=0.9924, R=0.9924, F1=0.9924, support=263
- Upstairs: P=0.9924, R=0.9886, F1=0.9905, support=264
- Downstairs: P=0.9924, R=0.9924, F1=0.9924, support=264
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=264
- Standing: P=1.0000, R=1.0000, F1=1.0000, support=263
