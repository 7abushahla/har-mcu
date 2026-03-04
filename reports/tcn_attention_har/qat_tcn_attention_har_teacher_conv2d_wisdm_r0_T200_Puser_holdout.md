# QAT_TCN_ATTENTION_HAR_TEACHER_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=user_holdout)

- Model: `/home/dellio/github/har-mcu/models_tflite/tcn_attention_har_teacher_conv2d_T200_Puser_holdout_wisdm_r0_qat.tflite`
- Model size: 631.39 KB
- Accuracy: 0.8710
- Macro-F1: 0.8169

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 21
- Interpreter ops: `['ADD', 'BATCH_MATMUL', 'BATCH_TO_SPACE_ND', 'CONCATENATION', 'CONV_2D', 'FILL', 'FULLY_CONNECTED', 'MEAN', 'MUL', 'PACK', 'PAD', 'REDUCE_PROD', 'RESHAPE', 'RSQRT', 'SHAPE', 'SOFTMAX', 'SPACE_TO_BATCH_ND', 'SQUARED_DIFFERENCE', 'STRIDED_SLICE', 'SUB', 'TRANSPOSE']`
- Inference latency median: 10.739 ms/sample
- Inference latency p95: 10.954 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/tcn_attention_har/confusion_qat_tcn_attention_har_teacher_conv2d_wisdm_r0_T200_Puser_holdout.png`

## Per-class metrics

- Walking: P=0.9758, R=0.8170, F1=0.8893, support=1333
- Jogging: P=0.9752, R=0.9769, F1=0.9760, support=1126
- Upstairs: P=0.6232, R=0.7549, F1=0.6828, support=412
- Downstairs: P=0.6952, R=0.8561, F1=0.7673, support=285
- Sitting: P=0.7448, R=0.8504, F1=0.7941, support=127
- Standing: P=0.6901, R=0.9291, F1=0.7919, support=127
