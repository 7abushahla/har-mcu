# ON_PTQ_DAGHERO_CNN_2LAYER_CONV2D_E05_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/accel_rotation_v2_bounded20_p025/daghero_cnn_2layer_conv2d/e05/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E05_daghero_cnn_2layer_conv2d_r0_ptq_int8.tflite`
- Model size: 26.13 KB
- Accuracy: 0.5234
- Macro-F1: 0.4880

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/on/daghero_cnn_2layer_conv2d/e05/confusion_on_ptq_daghero_cnn_2layer_conv2d_e05_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.4928, R=0.1288, F1=0.2042, support=264
- Jogging: P=0.9800, R=0.5589, F1=0.7119, support=263
- Upstairs: P=0.2919, R=0.8902, F1=0.4397, support=264
- Downstairs: P=0.5556, R=0.0568, F1=0.1031, support=264
- Sitting: P=0.6633, R=1.0000, F1=0.7976, support=264
- Standing: P=1.0000, R=0.5057, F1=0.6717, support=263
