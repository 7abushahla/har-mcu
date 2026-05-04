# FP32_TFLITE_DAGHERO_CNN_2LAYER_CONV2D_E00_DAGHERO_CNN_2LAYER_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/no_accel_rotation_v2/daghero_cnn_2layer_conv2d/e00/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E00_daghero_cnn_2layer_conv2d_r0_fp32.tflite`
- Model size: 80.41 KB
- Accuracy: 0.9922
- Macro-F1: 0.9895

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 0.040 ms/sample
- Inference latency p95: 0.056 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/no_accel_rotation_v2/daghero_cnn_2layer_conv2d/e00/m3/confusion_fp32_tflite_daghero_cnn_2layer_conv2d_E00_daghero_cnn_2layer_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9989, R=0.9941, F1=0.9965, support=2723
- Jogging: P=0.9957, R=0.9972, F1=0.9964, support=2109
- Upstairs: P=0.9662, R=0.9795, F1=0.9728, support=730
- Downstairs: P=0.9745, R=0.9761, F1=0.9753, support=587
- Sitting: P=1.0000, R=0.9948, F1=0.9974, support=381
- Standing: P=0.9967, R=1.0000, F1=0.9984, support=304
