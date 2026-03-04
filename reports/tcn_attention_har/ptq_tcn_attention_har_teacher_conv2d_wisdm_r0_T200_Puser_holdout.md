# PTQ_TCN_ATTENTION_HAR_TEACHER_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=user_holdout)

- Model: `/home/dellio/github/har-mcu/models_tflite/tcn_attention_har_teacher_conv2d_T200_Puser_holdout_wisdm_r0_ptq_int8.tflite`
- Model size: 623.99 KB
- Accuracy: 0.8633
- Macro-F1: 0.7985

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 21
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'BATCH_TO_SPACE_ND', 'CONCATENATION', 'CONV_2D', 'FILL', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'PACK', 'PAD', 'REDUCE_PROD', 'RESHAPE', 'RSQRT', 'SHAPE', 'SOFTMAX', 'SPACE_TO_BATCH_ND', 'SQUARED_DIFFERENCE', 'STRIDED_SLICE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 10.646 ms/sample
- Inference latency p95: 10.927 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/tcn_attention_har/confusion_ptq_tcn_attention_har_teacher_conv2d_wisdm_r0_T200_Puser_holdout.png`

## Per-class metrics

- Walking: P=0.9782, R=0.8080, F1=0.8850, support=1333
- Jogging: P=0.9753, R=0.9822, F1=0.9788, support=1126
- Upstairs: P=0.6867, R=0.6650, F1=0.6757, support=412
- Downstairs: P=0.6042, R=0.9158, F1=0.7280, support=285
- Sitting: P=0.7826, R=0.8504, F1=0.8151, support=127
- Standing: P=0.5728, R=0.9291, F1=0.7087, support=127
