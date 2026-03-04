# QAT_TCN_INCEPTION_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=user_holdout)

- Model: `/home/dellio/github/har-mcu/models_tflite/tcn_inception_conv2d_T200_Puser_holdout_wisdm_r0_qat.tflite`
- Model size: 384.81 KB
- Accuracy: 0.8431
- Macro-F1: 0.8026

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 15
- Interpreter ops: `['ADD', 'BATCH_TO_SPACE_ND', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'MUL', 'PACK', 'PAD', 'RESHAPE', 'SHAPE', 'SOFTMAX', 'SPACE_TO_BATCH_ND', 'STRIDED_SLICE']`
- Inference latency median: 3.268 ms/sample
- Inference latency p95: 3.333 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/tcn_inception/confusion_qat_tcn_inception_conv2d_wisdm_r0_T200_Puser_holdout.png`

## Per-class metrics

- Walking: P=0.9864, R=0.7607, F1=0.8590, support=1333
- Jogging: P=0.9693, R=0.9520, F1=0.9606, support=1126
- Upstairs: P=0.6362, R=0.7937, F1=0.7063, support=412
- Downstairs: P=0.5011, R=0.8351, F1=0.6263, support=285
- Sitting: P=0.9000, R=0.8504, F1=0.8745, support=127
- Standing: P=0.6946, R=0.9134, F1=0.7891, support=127
