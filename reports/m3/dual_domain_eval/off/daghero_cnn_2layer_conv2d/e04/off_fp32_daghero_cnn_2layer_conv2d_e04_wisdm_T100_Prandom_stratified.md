# OFF_FP32_DAGHERO_CNN_2LAYER_CONV2D_E04_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/no_accel_rotation/daghero_cnn_2layer_conv2d/e04/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E04_daghero_cnn_2layer_conv2d_r0_fp32.tflite`
- Model size: 80.41 KB
- Accuracy: 0.9921
- Macro-F1: 0.9895

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/daghero_cnn_2layer_conv2d/e04/confusion_off_fp32_daghero_cnn_2layer_conv2d_e04_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9978, R=0.9941, F1=0.9960, support=2723
- Jogging: P=0.9953, R=0.9972, F1=0.9962, support=2109
- Upstairs: P=0.9688, R=0.9795, F1=0.9741, support=730
- Downstairs: P=0.9761, R=0.9744, F1=0.9753, support=587
- Sitting: P=1.0000, R=0.9948, F1=0.9974, support=381
- Standing: P=0.9967, R=1.0000, F1=0.9984, support=304
