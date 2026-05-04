# OFF_PTQ_DAGHERO_CNN_2LAYER_CONV2D_E06_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E06_no_norm_matched/no_accel_rotation/daghero_cnn_2layer_conv2d/e06/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E06_daghero_cnn_2layer_conv2d_r0_ptq_int8.tflite`
- Model size: 26.13 KB
- Accuracy: 0.9933
- Macro-F1: 0.9906

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/daghero_cnn_2layer_conv2d/e06/confusion_off_ptq_daghero_cnn_2layer_conv2d_e06_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9952, R=0.9978, F1=0.9965, support=2723
- Jogging: P=0.9957, R=0.9995, F1=0.9976, support=2109
- Upstairs: P=0.9834, R=0.9740, F1=0.9787, support=730
- Downstairs: P=0.9810, R=0.9693, F1=0.9751, support=587
- Sitting: P=1.0000, R=0.9948, F1=0.9974, support=381
- Standing: P=0.9967, R=1.0000, F1=0.9984, support=304
