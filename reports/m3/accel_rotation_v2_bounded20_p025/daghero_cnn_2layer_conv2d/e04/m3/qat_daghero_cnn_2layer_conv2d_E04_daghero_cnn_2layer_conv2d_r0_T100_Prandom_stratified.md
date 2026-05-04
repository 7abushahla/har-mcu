# QAT_DAGHERO_CNN_2LAYER_CONV2D_E04_DAGHERO_CNN_2LAYER_CONV2D_R0 TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/accel_rotation_v2_bounded20_p025/daghero_cnn_2layer_conv2d/e04/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E04_daghero_cnn_2layer_conv2d_r0_qat.tflite`
- Model size: 26.73 KB
- Accuracy: 0.5164
- Macro-F1: 0.4688

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Inference latency median: 0.077 ms/sample
- Inference latency p95: 0.094 ms/sample
- Timed samples: 256
- Warmup samples: 32
- Confusion matrix plot: `/shared/b00088568/github/har-mcu/reports/m3/accel_rotation_v2_bounded20_p025/daghero_cnn_2layer_conv2d/e04/m3/confusion_qat_daghero_cnn_2layer_conv2d_E04_daghero_cnn_2layer_conv2d_r0_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.5333, R=0.0303, F1=0.0573, support=264
- Jogging: P=0.9808, R=0.5817, F1=0.7303, support=263
- Upstairs: P=0.2852, R=0.9129, F1=0.4346, support=264
- Downstairs: P=0.5000, R=0.0682, F1=0.1200, support=264
- Sitting: P=0.6650, R=1.0000, F1=0.7988, support=264
- Standing: P=1.0000, R=0.5057, F1=0.6717, support=263
