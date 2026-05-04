# ON_FP32_DAGHERO_CNN_2LAYER_CONV2D_E08_ARDUINO TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E08_T50_window/accel_rotation_v3_target_clusters_p025/daghero_cnn_2layer_conv2d/e08/daghero_cnn_2layer_conv2d_T50_Prandom_stratified_E08_daghero_cnn_2layer_conv2d_r0_fp32.tflite`
- Model size: 80.41 KB
- Accuracy: 0.1666
- Macro-F1: 0.0476

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/daghero_cnn_2layer_conv2d/e08/confusion_on_fp32_daghero_cnn_2layer_conv2d_e08_arduino_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.0000, R=0.0000, F1=0.0000, support=529
- Jogging: P=0.0000, R=0.0000, F1=0.0000, support=528
- Upstairs: P=0.0000, R=0.0000, F1=0.0000, support=529
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=528
- Sitting: P=0.0000, R=0.0000, F1=0.0000, support=528
- Standing: P=0.1666, R=1.0000, F1=0.2856, support=528
