# OFF_FP32_DAGHERO_CNN_2LAYER_CONV2D_E06_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E06_no_norm_matched/no_accel_rotation_v2/daghero_cnn_2layer_conv2d/e06/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E06_daghero_cnn_2layer_conv2d_r0_fp32.tflite`
- Model size: 80.41 KB
- Accuracy: 0.9943
- Macro-F1: 0.9918

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/off/daghero_cnn_2layer_conv2d/e06/confusion_off_fp32_daghero_cnn_2layer_conv2d_e06_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9971, R=0.9974, F1=0.9972, support=2723
- Jogging: P=0.9972, R=0.9991, F1=0.9981, support=2109
- Upstairs: P=0.9796, R=0.9863, F1=0.9829, support=730
- Downstairs: P=0.9844, R=0.9693, F1=0.9768, support=587
- Sitting: P=1.0000, R=0.9948, F1=0.9974, support=381
- Standing: P=0.9967, R=1.0000, F1=0.9984, support=304
