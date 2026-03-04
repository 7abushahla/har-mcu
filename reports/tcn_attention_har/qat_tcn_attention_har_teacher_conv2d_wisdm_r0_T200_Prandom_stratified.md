# QAT_TCN_ATTENTION_HAR_TEACHER_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=random_stratified)

- Model: `/home/dellio/github/har-mcu/models_tflite/tcn_attention_har_teacher_conv2d_T200_Prandom_stratified_wisdm_r0_qat.tflite`
- Model size: 631.39 KB
- Accuracy: 0.9964
- Macro-F1: 0.9929

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 21
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'BATCH_TO_SPACE_ND', 'CONCATENATION', 'CONV_2D', 'FILL', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'PACK', 'PAD', 'REDUCE_PROD', 'RESHAPE', 'RSQRT', 'SHAPE', 'SOFTMAX', 'SPACE_TO_BATCH_ND', 'SQUARED_DIFFERENCE', 'STRIDED_SLICE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 11.012 ms/sample
- Inference latency p95: 11.393 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/tcn_attention_har/confusion_qat_tcn_attention_har_teacher_conv2d_wisdm_r0_T200_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9985, R=0.9993, F1=0.9989, support=1344
- Jogging: P=0.9971, R=1.0000, F1=0.9986, support=1037
- Upstairs: P=0.9939, R=0.9909, F1=0.9924, support=328
- Downstairs: P=0.9921, R=0.9805, F1=0.9862, support=256
- Sitting: P=0.9891, R=0.9945, F1=0.9918, support=182
- Standing: P=0.9931, R=0.9862, F1=0.9896, support=145
