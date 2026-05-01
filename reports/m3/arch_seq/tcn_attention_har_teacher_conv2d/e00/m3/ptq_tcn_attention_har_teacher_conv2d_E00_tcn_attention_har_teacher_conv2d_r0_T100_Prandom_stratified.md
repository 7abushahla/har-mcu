# PTQ_TCN_ATTENTION_HAR_TEACHER_CONV2D_E00_TCN_ATTENTION_HAR_TEACHER_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00090279/TinyML-Course/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/arch_seq/tcn_attention_har_teacher_conv2d/e00/tcn_attention_har_teacher_conv2d_T100_Prandom_stratified_E00_tcn_attention_har_teacher_conv2d_r0_ptq_int8.tflite`
- Model size: 578.40 KB
- Accuracy: 0.9939
- Macro-F1: 0.9909

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 14
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'PAD', 'RESHAPE', 'RSQRT', 'SOFTMAX', 'SQUARED_DIFFERENCE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 8.258 ms/sample
- Inference latency p95: 8.572 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00090279/TinyML-Course/har-mcu/reports/m3/arch_seq/tcn_attention_har_teacher_conv2d/e00/m3/confusion_ptq_tcn_attention_har_teacher_conv2d_E00_tcn_attention_har_teacher_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9985, R=0.9967, F1=0.9976, support=2723
- Jogging: P=0.9972, R=0.9986, F1=0.9979, support=2109
- Upstairs: P=0.9875, R=0.9726, F1=0.9800, support=730
- Downstairs: P=0.9650, R=0.9864, F1=0.9756, support=587
- Sitting: P=0.9974, R=0.9974, F1=0.9974, support=381
- Standing: P=0.9967, R=0.9967, F1=0.9967, support=304
