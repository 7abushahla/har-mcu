# PTQ_TCN_INCEPTION_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=random_stratified)

- Model: `/home/dellio/github/har-mcu/models_tflite/tcn_inception_conv2d_T200_Prandom_stratified_wisdm_r0_ptq_int8.tflite`
- Model size: 379.45 KB
- Accuracy: 0.9976
- Macro-F1: 0.9946

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 15
- Interpreter ops: `['ADD', 'BATCH_TO_SPACE_ND', 'CONCATENATION', 'CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'MUL', 'PACK', 'PAD', 'RESHAPE', 'SHAPE', 'SOFTMAX', 'SPACE_TO_BATCH_ND', 'STRIDED_SLICE']`
- Inference latency median: 3.013 ms/sample
- Inference latency p95: 3.056 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/tcn_inception/confusion_ptq_tcn_inception_conv2d_wisdm_r0_T200_Prandom_stratified.png`

## Per-class metrics

- Walking: P=1.0000, R=0.9993, F1=0.9996, support=1344
- Jogging: P=1.0000, R=0.9990, F1=0.9995, support=1037
- Upstairs: P=0.9850, R=1.0000, F1=0.9924, support=328
- Downstairs: P=0.9961, R=0.9922, F1=0.9941, support=256
- Sitting: P=1.0000, R=0.9780, F1=0.9889, support=182
- Standing: P=0.9864, R=1.0000, F1=0.9932, support=145
