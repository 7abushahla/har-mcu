# OFF_FP32_DAGHERO_CNN_2LAYER_CONV2D_E08_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E08_T50_window/no_accel_rotation/daghero_cnn_2layer_conv2d/e08/daghero_cnn_2layer_conv2d_T50_Prandom_stratified_E08_daghero_cnn_2layer_conv2d_r0_fp32.tflite`
- Model size: 80.41 KB
- Accuracy: 0.9851
- Macro-F1: 0.9797

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/daghero_cnn_2layer_conv2d/e08/confusion_off_fp32_daghero_cnn_2layer_conv2d_e08_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9927, R=0.9945, F1=0.9936, support=5482
- Jogging: P=0.9886, R=0.9974, F1=0.9930, support=4250
- Upstairs: P=0.9801, R=0.9247, F1=0.9516, support=1541
- Downstairs: P=0.9362, R=0.9640, F1=0.9499, support=1249
- Sitting: P=0.9936, R=0.9936, F1=0.9936, support=777
- Standing: P=0.9952, R=0.9984, F1=0.9968, support=624
