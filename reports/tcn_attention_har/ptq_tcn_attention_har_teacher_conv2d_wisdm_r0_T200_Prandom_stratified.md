# PTQ_TCN_ATTENTION_HAR_TEACHER_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=random_stratified)

- Model: `/home/dellio/github/har-mcu/models_tflite/tcn_attention_har_teacher_conv2d_T200_Prandom_stratified_wisdm_r0_ptq_int8.tflite`
- Model size: 623.99 KB
- Accuracy: 0.9948
- Macro-F1: 0.9890

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 21
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'BATCH_TO_SPACE_ND', 'CONCATENATION', 'CONV_2D', 'FILL', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'PACK', 'PAD', 'REDUCE_PROD', 'RESHAPE', 'RSQRT', 'SHAPE', 'SOFTMAX', 'SPACE_TO_BATCH_ND', 'SQUARED_DIFFERENCE', 'STRIDED_SLICE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 11.107 ms/sample
- Inference latency p95: 11.540 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/tcn_attention_har/confusion_ptq_tcn_attention_har_teacher_conv2d_wisdm_r0_T200_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9985, R=0.9985, F1=0.9985, support=1344
- Jogging: P=0.9990, R=1.0000, F1=0.9995, support=1037
- Upstairs: P=0.9878, R=0.9878, F1=0.9878, support=328
- Downstairs: P=0.9767, R=0.9805, F1=0.9786, support=256
- Sitting: P=0.9835, R=0.9835, F1=0.9835, support=182
- Standing: P=0.9930, R=0.9793, F1=0.9861, support=145
