# PTQ_TCN_ATTENTION_HAR_TEACHER_CONV2D_E06_TCN_ATTENTION_HAR_TEACHER_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E06_no_norm_matched/arch_seq/tcn_attention_har_teacher_conv2d/e06/tcn_attention_har_teacher_conv2d_T100_Prandom_stratified_E06_tcn_attention_har_teacher_conv2d_r0_ptq_int8.tflite`
- Model size: 578.40 KB
- Accuracy: 0.4305
- Macro-F1: 0.3940

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 14
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'PAD', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 8.223 ms/sample
- Inference latency p95: 8.646 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/tcn_attention_har_teacher_conv2d/e06/m3/confusion_ptq_tcn_attention_har_teacher_conv2d_E06_tcn_attention_har_teacher_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.3333, R=0.2386, F1=0.2781, support=264
- Jogging: P=0.0000, R=0.0000, F1=0.0000, support=263
- Upstairs: P=0.1449, R=0.0379, F1=0.0601, support=264
- Downstairs: P=0.2276, R=0.7992, F1=0.3543, support=264
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=264
- Standing: P=1.0000, R=0.5057, F1=0.6717, support=263
