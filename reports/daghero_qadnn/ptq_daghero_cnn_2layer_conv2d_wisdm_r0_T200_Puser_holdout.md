# PTQ_DAGHERO_CNN_2LAYER_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=user_holdout)

- Model: `/home/dellio/github/har-mcu/models_tflite/daghero_cnn_2layer_conv2d_T200_Puser_holdout_wisdm_r0_ptq_int8.tflite`
- Model size: 27.37 KB
- Accuracy: 0.8235
- Macro-F1: 0.7658

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 9
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'PACK', 'RESHAPE', 'SHAPE', 'SOFTMAX', 'STRIDED_SLICE']`
- Inference latency median: 0.090 ms/sample
- Inference latency p95: 0.103 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/daghero_qadnn/confusion_ptq_daghero_cnn_2layer_conv2d_wisdm_r0_T200_Puser_holdout.png`

## Per-class metrics

- Walking: P=0.9729, R=0.8080, F1=0.8828, support=1333
- Jogging: P=0.9765, R=0.9236, F1=0.9493, support=1126
- Upstairs: P=0.5165, R=0.7597, F1=0.6149, support=412
- Downstairs: P=0.4469, R=0.5018, F1=0.4727, support=285
- Sitting: P=0.9310, R=0.8504, F1=0.8889, support=127
- Standing: P=0.6480, R=1.0000, F1=0.7864, support=127
