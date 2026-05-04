# FP32_TFLITE_DAGHERO_CNN_2LAYER_CONV2D_E12_DAGHERO_CNN_2LAYER_CONV2D_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/no_accel_rotation/daghero_cnn_2layer_conv2d/e12/daghero_cnn_2layer_conv2d_T50_Prandom_stratified_E12_daghero_cnn_2layer_conv2d_r0_fp32.tflite`
- Model size: 80.41 KB
- Accuracy: 0.9880
- Macro-F1: 0.9880

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 0.023 ms/sample
- Inference latency p95: 0.027 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/no_accel_rotation/daghero_cnn_2layer_conv2d/e12/m3/confusion_fp32_tflite_daghero_cnn_2layer_conv2d_E12_daghero_cnn_2layer_conv2d_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9869, R=0.9981, F1=0.9925, support=529
- Jogging: P=0.9981, R=0.9905, F1=0.9943, support=528
- Upstairs: P=0.9788, R=0.9584, F1=0.9685, support=529
- Downstairs: P=0.9646, R=0.9811, F1=0.9728, support=528
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=528
- Standing: P=1.0000, R=1.0000, F1=1.0000, support=528
