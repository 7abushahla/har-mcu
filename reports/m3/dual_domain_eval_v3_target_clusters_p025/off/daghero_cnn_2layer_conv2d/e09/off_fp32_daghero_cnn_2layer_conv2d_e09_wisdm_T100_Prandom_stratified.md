# OFF_FP32_DAGHERO_CNN_2LAYER_CONV2D_E09_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/no_accel_rotation_v2/daghero_cnn_2layer_conv2d/e09/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E09_daghero_cnn_2layer_conv2d_r0_fp32.tflite`
- Model size: 80.41 KB
- Accuracy: 0.3598
- Macro-F1: 0.2209

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/off/daghero_cnn_2layer_conv2d/e09/confusion_off_fp32_daghero_cnn_2layer_conv2d_e09_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.0000, R=0.0000, F1=0.0000, support=2723
- Jogging: P=0.3704, R=1.0000, F1=0.5406, support=2109
- Upstairs: P=0.2253, R=0.2808, F1=0.2500, support=730
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=587
- Sitting: P=0.9006, R=0.3806, F1=0.5351, support=381
- Standing: P=0.0000, R=0.0000, F1=0.0000, support=304
