# OFF_PTQ_DAGHERO_CNN_2LAYER_CONV2D_E05_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/no_accel_rotation_v2/daghero_cnn_2layer_conv2d/e05/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E05_daghero_cnn_2layer_conv2d_r0_ptq_int8.tflite`
- Model size: 26.13 KB
- Accuracy: 0.5013
- Macro-F1: 0.4422

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/off/daghero_cnn_2layer_conv2d/e05/confusion_off_ptq_daghero_cnn_2layer_conv2d_e05_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.6429, R=0.0341, F1=0.0647, support=264
- Jogging: P=1.0000, R=0.4753, F1=0.6443, support=263
- Upstairs: P=0.2848, R=0.9773, F1=0.4410, support=264
- Downstairs: P=0.4000, R=0.0152, F1=0.0292, support=264
- Sitting: P=0.6701, R=1.0000, F1=0.8024, support=264
- Standing: P=1.0000, R=0.5057, F1=0.6717, support=263
