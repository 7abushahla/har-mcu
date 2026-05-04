# FP32_TFLITE_DAGHERO_CNN_2LAYER_CONV2D_E04_DAGHERO_CNN_2LAYER_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/no_accel_rotation/daghero_cnn_2layer_conv2d/e04/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E04_daghero_cnn_2layer_conv2d_r0_fp32.tflite`
- Model size: 80.41 KB
- Accuracy: 0.5095
- Macro-F1: 0.4533

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 0.040 ms/sample
- Inference latency p95: 0.048 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/no_accel_rotation/daghero_cnn_2layer_conv2d/e04/m3/confusion_fp32_tflite_daghero_cnn_2layer_conv2d_E04_daghero_cnn_2layer_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.6667, R=0.0530, F1=0.0982, support=264
- Jogging: P=1.0000, R=0.5057, F1=0.6717, support=263
- Upstairs: P=0.2902, R=0.9773, F1=0.4475, support=264
- Downstairs: P=0.3636, R=0.0152, F1=0.0291, support=264
- Sitting: P=0.6684, R=1.0000, F1=0.8012, support=264
- Standing: P=1.0000, R=0.5057, F1=0.6717, support=263
