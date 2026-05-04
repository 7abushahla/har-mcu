# QAT_DAGHERO_CNN_2LAYER_CONV2D_E08_DAGHERO_CNN_2LAYER_CONV2D_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E08_T50_window/no_accel_rotation_v2/daghero_cnn_2layer_conv2d/e08/daghero_cnn_2layer_conv2d_T50_Prandom_stratified_E08_daghero_cnn_2layer_conv2d_r0_qat.tflite`
- Model size: 26.73 KB
- Accuracy: 0.1666
- Macro-F1: 0.0476

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 0.044 ms/sample
- Inference latency p95: 0.051 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/no_accel_rotation_v2/daghero_cnn_2layer_conv2d/e08/m3/confusion_qat_daghero_cnn_2layer_conv2d_E08_daghero_cnn_2layer_conv2d_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.0000, R=0.0000, F1=0.0000, support=529
- Jogging: P=0.0000, R=0.0000, F1=0.0000, support=528
- Upstairs: P=0.0000, R=0.0000, F1=0.0000, support=529
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=528
- Sitting: P=0.0000, R=0.0000, F1=0.0000, support=528
- Standing: P=0.1666, R=1.0000, F1=0.2856, support=528
