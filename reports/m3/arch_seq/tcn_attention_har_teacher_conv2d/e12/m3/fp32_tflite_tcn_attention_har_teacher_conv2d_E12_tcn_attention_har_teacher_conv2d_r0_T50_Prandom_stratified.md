# FP32_TFLITE_TCN_ATTENTION_HAR_TEACHER_CONV2D_E12_TCN_ATTENTION_HAR_TEACHER_CONV2D_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/arch_seq/tcn_attention_har_teacher_conv2d/e12/tcn_attention_har_teacher_conv2d_T50_Prandom_stratified_E12_tcn_attention_har_teacher_conv2d_r0_fp32.tflite`
- Model size: 1883.16 KB
- Accuracy: 0.9785
- Macro-F1: 0.9785

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 14
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'PAD', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 1.128 ms/sample
- Inference latency p95: 1.176 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/tcn_attention_har_teacher_conv2d/e12/m3/confusion_fp32_tflite_tcn_attention_har_teacher_conv2d_E12_tcn_attention_har_teacher_conv2d_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9925, R=0.9962, F1=0.9943, support=529
- Jogging: P=0.9905, R=0.9867, F1=0.9886, support=528
- Upstairs: P=0.9397, R=0.9433, F1=0.9415, support=529
- Downstairs: P=0.9505, R=0.9451, F1=0.9478, support=528
- Sitting: P=0.9981, R=1.0000, F1=0.9991, support=528
- Standing: P=1.0000, R=1.0000, F1=1.0000, support=528
