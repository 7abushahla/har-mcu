# PTQ_DAGHERO_CNN_2LAYER_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=random_stratified)

- Model: `/home/dellio/github/har-mcu/models_tflite/daghero_cnn_2layer_conv2d_T200_Prandom_stratified_wisdm_r0_ptq_int8.tflite`
- Model size: 27.37 KB
- Accuracy: 0.9939
- Macro-F1: 0.9875

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 9
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'PACK', 'RESHAPE', 'SHAPE', 'SOFTMAX', 'STRIDED_SLICE']`
- Inference latency median: 0.090 ms/sample
- Inference latency p95: 0.103 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/daghero_qadnn/confusion_ptq_daghero_cnn_2layer_conv2d_wisdm_r0_T200_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9993, R=0.9978, F1=0.9985, support=1344
- Jogging: P=0.9962, R=0.9990, F1=0.9976, support=1037
- Upstairs: P=0.9789, R=0.9878, F1=0.9833, support=328
- Downstairs: P=0.9921, R=0.9844, F1=0.9882, support=256
- Sitting: P=1.0000, R=0.9560, F1=0.9775, support=182
- Standing: P=0.9603, R=1.0000, F1=0.9797, support=145
