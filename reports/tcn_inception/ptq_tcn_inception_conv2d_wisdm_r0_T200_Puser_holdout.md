# PTQ_TCN_INCEPTION_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=user_holdout)

- Model: `/home/dellio/github/har-mcu/models_tflite/tcn_inception_conv2d_T200_Puser_holdout_wisdm_r0_ptq_int8.tflite`
- Model size: 379.45 KB
- Accuracy: 0.8138
- Macro-F1: 0.7434

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 15
- Interpreter ops: `['ADD', 'BATCH_TO_SPACE_ND', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'MUL', 'PACK', 'PAD', 'RESHAPE', 'SHAPE', 'SOFTMAX', 'SPACE_TO_BATCH_ND', 'STRIDED_SLICE']`
- Inference latency median: 3.062 ms/sample
- Inference latency p95: 3.160 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/tcn_inception/confusion_ptq_tcn_inception_conv2d_wisdm_r0_T200_Puser_holdout.png`

## Per-class metrics

- Walking: P=0.9027, R=0.8215, F1=0.8602, support=1333
- Jogging: P=0.9671, R=0.9396, F1=0.9532, support=1126
- Upstairs: P=0.4696, R=0.6942, F1=0.5602, support=412
- Downstairs: P=0.6404, R=0.4000, F1=0.4924, support=285
- Sitting: P=0.9815, R=0.8346, F1=0.9021, support=127
- Standing: P=0.5577, R=0.9134, F1=0.6925, support=127
