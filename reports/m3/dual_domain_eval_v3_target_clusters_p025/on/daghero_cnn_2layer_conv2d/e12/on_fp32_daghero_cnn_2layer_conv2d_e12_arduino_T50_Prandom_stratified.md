# ON_FP32_DAGHERO_CNN_2LAYER_CONV2D_E12_ARDUINO TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/accel_rotation_v3_target_clusters_p025/daghero_cnn_2layer_conv2d/e12/daghero_cnn_2layer_conv2d_T50_Prandom_stratified_E12_daghero_cnn_2layer_conv2d_r0_fp32.tflite`
- Model size: 80.41 KB
- Accuracy: 0.9836
- Macro-F1: 0.9836

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/daghero_cnn_2layer_conv2d/e12/confusion_on_fp32_daghero_cnn_2layer_conv2d_e12_arduino_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9888, R=0.9981, F1=0.9934, support=529
- Jogging: P=1.0000, R=0.9867, F1=0.9933, support=528
- Upstairs: P=0.9617, R=0.9490, F1=0.9553, support=529
- Downstairs: P=0.9534, R=0.9678, F1=0.9605, support=528
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=528
- Standing: P=0.9981, R=1.0000, F1=0.9991, support=528
