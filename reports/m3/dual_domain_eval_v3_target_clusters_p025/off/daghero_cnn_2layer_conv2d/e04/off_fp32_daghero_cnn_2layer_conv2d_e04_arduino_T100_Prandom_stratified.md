# OFF_FP32_DAGHERO_CNN_2LAYER_CONV2D_E04_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/no_accel_rotation_v2/daghero_cnn_2layer_conv2d/e04/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E04_daghero_cnn_2layer_conv2d_r0_fp32.tflite`
- Model size: 80.41 KB
- Accuracy: 0.5107
- Macro-F1: 0.4545

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/off/daghero_cnn_2layer_conv2d/e04/confusion_off_fp32_daghero_cnn_2layer_conv2d_e04_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.6087, R=0.0530, F1=0.0976, support=264
- Jogging: P=1.0000, R=0.5133, F1=0.6784, support=263
- Upstairs: P=0.2915, R=0.9773, F1=0.4491, support=264
- Downstairs: P=0.3636, R=0.0152, F1=0.0291, support=264
- Sitting: P=0.6684, R=1.0000, F1=0.8012, support=264
- Standing: P=1.0000, R=0.5057, F1=0.6717, support=263
