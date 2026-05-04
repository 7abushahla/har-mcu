# OFF_PTQ_DAGHERO_CNN_2LAYER_CONV2D_E12_ARDUINO TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/no_accel_rotation_v2/daghero_cnn_2layer_conv2d/e12/daghero_cnn_2layer_conv2d_T50_Prandom_stratified_E12_daghero_cnn_2layer_conv2d_r0_ptq_int8.tflite`
- Model size: 26.13 KB
- Accuracy: 0.9877
- Macro-F1: 0.9877

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/off/daghero_cnn_2layer_conv2d/e12/confusion_off_ptq_daghero_cnn_2layer_conv2d_e12_arduino_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9869, R=0.9981, F1=0.9925, support=529
- Jogging: P=0.9981, R=0.9905, F1=0.9943, support=528
- Upstairs: P=0.9732, R=0.9622, F1=0.9677, support=529
- Downstairs: P=0.9680, R=0.9754, F1=0.9717, support=528
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=528
- Standing: P=1.0000, R=1.0000, F1=1.0000, support=528
