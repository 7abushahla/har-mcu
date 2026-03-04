# QAT_DAGHERO_CNN_2LAYER_CONV2D_WISDM_R0 TFLite Evaluation (T=200, protocol=random_stratified)

- Model: `/home/dellio/github/har-mcu/models_tflite/daghero_cnn_2layer_conv2d_T200_Prandom_stratified_wisdm_r0_qat.tflite`
- Model size: 29.41 KB
- Accuracy: 0.9924
- Macro-F1: 0.9851

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 11
- Interpreter ops: `['ADD', 'CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'MUL', 'PACK', 'RESHAPE', 'SHAPE', 'SOFTMAX', 'STRIDED_SLICE']`
- Inference latency median: 0.116 ms/sample
- Inference latency p95: 0.145 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/home/dellio/github/har-mcu/reports/daghero_qadnn/confusion_qat_daghero_cnn_2layer_conv2d_wisdm_r0_T200_Prandom_stratified.png`

## Per-class metrics

- Walking: P=1.0000, R=0.9970, F1=0.9985, support=1344
- Jogging: P=0.9942, R=1.0000, F1=0.9971, support=1037
- Upstairs: P=0.9815, R=0.9726, F1=0.9770, support=328
- Downstairs: P=0.9691, R=0.9805, F1=0.9748, support=256
- Sitting: P=1.0000, R=0.9615, F1=0.9804, support=182
- Standing: P=0.9667, R=1.0000, F1=0.9831, support=145
