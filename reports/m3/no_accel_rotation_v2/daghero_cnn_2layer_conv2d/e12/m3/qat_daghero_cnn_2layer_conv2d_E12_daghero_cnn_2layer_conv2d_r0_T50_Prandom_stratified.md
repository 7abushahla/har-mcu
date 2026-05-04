# QAT_DAGHERO_CNN_2LAYER_CONV2D_E12_DAGHERO_CNN_2LAYER_CONV2D_R0 TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/no_accel_rotation_v2/daghero_cnn_2layer_conv2d/e12/daghero_cnn_2layer_conv2d_T50_Prandom_stratified_E12_daghero_cnn_2layer_conv2d_r0_qat.tflite`
- Model size: 26.73 KB
- Accuracy: 0.9880
- Macro-F1: 0.9880

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 0.045 ms/sample
- Inference latency p95: 0.054 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/no_accel_rotation_v2/daghero_cnn_2layer_conv2d/e12/m3/confusion_qat_daghero_cnn_2layer_conv2d_E12_daghero_cnn_2layer_conv2d_r0_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9851, R=0.9981, F1=0.9915, support=529
- Jogging: P=0.9943, R=0.9905, F1=0.9924, support=528
- Upstairs: P=0.9863, R=0.9509, F1=0.9682, support=529
- Downstairs: P=0.9631, R=0.9886, F1=0.9757, support=528
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=528
- Standing: P=1.0000, R=1.0000, F1=1.0000, support=528
