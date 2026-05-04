# OFF_QAT_DAGHERO_CNN_2LAYER_CONV2D_E03_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E03_arduino_downsample_20hz_T100/no_accel_rotation/daghero_cnn_2layer_conv2d/e03/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E03_daghero_cnn_2layer_conv2d_r0_qat.tflite`
- Model size: 26.73 KB
- Accuracy: 0.9931
- Macro-F1: 0.9903

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/daghero_cnn_2layer_conv2d/e03/confusion_off_qat_daghero_cnn_2layer_conv2d_e03_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9989, R=0.9949, F1=0.9969, support=2723
- Jogging: P=0.9953, R=1.0000, F1=0.9976, support=2109
- Upstairs: P=0.9728, R=0.9781, F1=0.9754, support=730
- Downstairs: P=0.9778, R=0.9744, F1=0.9761, support=587
- Sitting: P=1.0000, R=0.9948, F1=0.9974, support=381
- Standing: P=0.9967, R=1.0000, F1=0.9984, support=304
