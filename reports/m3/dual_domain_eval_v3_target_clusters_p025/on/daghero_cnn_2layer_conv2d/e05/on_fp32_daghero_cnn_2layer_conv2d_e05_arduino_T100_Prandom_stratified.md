# ON_FP32_DAGHERO_CNN_2LAYER_CONV2D_E05_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/accel_rotation_v3_target_clusters_p025/daghero_cnn_2layer_conv2d/e05/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E05_daghero_cnn_2layer_conv2d_r0_fp32.tflite`
- Model size: 80.41 KB
- Accuracy: 0.5164
- Macro-F1: 0.4600

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/daghero_cnn_2layer_conv2d/e05/confusion_on_fp32_daghero_cnn_2layer_conv2d_e05_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.4211, R=0.0606, F1=0.1060, support=264
- Jogging: P=0.9933, R=0.5665, F1=0.7215, support=263
- Upstairs: P=0.2943, R=0.9621, F1=0.4508, support=264
- Downstairs: P=0.2500, R=0.0038, F1=0.0075, support=264
- Sitting: P=0.6701, R=1.0000, F1=0.8024, support=264
- Standing: P=1.0000, R=0.5057, F1=0.6717, support=263
