# PTQ_TCN_ATTENTION_HAR_TEACHER_CONV2D_E12_TCN_ATTENTION_HAR_TEACHER_CONV2D_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/arch_seq/tcn_attention_har_teacher_conv2d/e12/tcn_attention_har_teacher_conv2d_T50_Prandom_stratified_E12_tcn_attention_har_teacher_conv2d_r0_ptq_int8.tflite`
- Model size: 578.35 KB
- Accuracy: 0.9779
- Macro-F1: 0.9779

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 14
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'PAD', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 4.255 ms/sample
- Inference latency p95: 4.425 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/tcn_attention_har_teacher_conv2d/e12/m3/confusion_ptq_tcn_attention_har_teacher_conv2d_E12_tcn_attention_har_teacher_conv2d_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9925, R=0.9962, F1=0.9943, support=529
- Jogging: P=0.9905, R=0.9867, F1=0.9886, support=528
- Upstairs: P=0.9362, R=0.9433, F1=0.9397, support=529
- Downstairs: P=0.9503, R=0.9413, F1=0.9458, support=528
- Sitting: P=0.9981, R=1.0000, F1=0.9991, support=528
- Standing: P=1.0000, R=1.0000, F1=1.0000, support=528
