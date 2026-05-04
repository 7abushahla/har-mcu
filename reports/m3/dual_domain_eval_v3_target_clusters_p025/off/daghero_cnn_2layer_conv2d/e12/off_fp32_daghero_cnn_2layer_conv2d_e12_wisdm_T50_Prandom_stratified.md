# OFF_FP32_DAGHERO_CNN_2LAYER_CONV2D_E12_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/no_accel_rotation_v2/daghero_cnn_2layer_conv2d/e12/daghero_cnn_2layer_conv2d_T50_Prandom_stratified_E12_daghero_cnn_2layer_conv2d_r0_fp32.tflite`
- Model size: 80.41 KB
- Accuracy: 0.3780
- Macro-F1: 0.2346

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/off/daghero_cnn_2layer_conv2d/e12/confusion_off_fp32_daghero_cnn_2layer_conv2d_e12_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.0000, R=0.0000, F1=0.0000, support=5482
- Jogging: P=0.4622, R=0.9668, F1=0.6254, support=4250
- Upstairs: P=0.1883, R=0.5762, F1=0.2839, support=1541
- Downstairs: P=0.0690, R=0.0016, F1=0.0031, support=1249
- Sitting: P=0.9135, R=0.3398, F1=0.4953, support=777
- Standing: P=0.0000, R=0.0000, F1=0.0000, support=624
