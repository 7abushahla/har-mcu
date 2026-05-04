# QAT_DAGHERO_CNN_2LAYER_CONV2D_E04_DAGHERO_CNN_2LAYER_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/accel_rotation_v3_target_clusters_p025/daghero_cnn_2layer_conv2d/e04/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E04_daghero_cnn_2layer_conv2d_r0_qat.tflite`
- Model size: 26.73 KB
- Accuracy: 0.5714
- Macro-F1: 0.5393

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 0.076 ms/sample
- Inference latency p95: 0.095 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/accel_rotation_v3_target_clusters_p025/daghero_cnn_2layer_conv2d/e04/m3/confusion_qat_daghero_cnn_2layer_conv2d_E04_daghero_cnn_2layer_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.4570, R=0.2614, F1=0.3325, support=264
- Jogging: P=1.0000, R=0.5475, F1=0.7076, support=263
- Upstairs: P=0.3065, R=0.8788, F1=0.4545, support=264
- Downstairs: P=0.3333, R=0.0038, F1=0.0075, support=264
- Sitting: P=0.7928, R=1.0000, F1=0.8844, support=264
- Standing: P=1.0000, R=0.7376, F1=0.8490, support=263
