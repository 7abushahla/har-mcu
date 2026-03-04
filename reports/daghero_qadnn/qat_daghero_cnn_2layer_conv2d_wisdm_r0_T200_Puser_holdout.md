# QAT_DAGHERO_CNN_2LAYER_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=user_holdout)

- Model: `/home/dellio/github/har-mcu/models_tflite/daghero_cnn_2layer_conv2d_T200_Puser_holdout_wisdm_r0_qat.tflite`
- Model size: 29.41 KB
- Accuracy: 0.8598
- Macro-F1: 0.8283

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 11
- Interpreter ops: `['ADD', 'CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'MUL', 'PACK', 'RESHAPE', 'SHAPE', 'SOFTMAX', 'STRIDED_SLICE']`
- Inference latency median: 0.115 ms/sample
- Inference latency p95: 0.128 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/daghero_qadnn/confusion_qat_daghero_cnn_2layer_conv2d_wisdm_r0_T200_Puser_holdout.png`

## Per-class metrics

- Walking: P=0.9745, R=0.8590, F1=0.9131, support=1333
- Jogging: P=0.9807, R=0.9041, F1=0.9409, support=1126
- Upstairs: P=0.5778, R=0.8738, F1=0.6957, support=412
- Downstairs: P=0.5469, R=0.6140, F1=0.5785, support=285
- Sitting: P=0.9908, R=0.8504, F1=0.9153, support=127
- Standing: P=0.8690, R=0.9921, F1=0.9265, support=127
