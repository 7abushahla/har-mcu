# OFF_QAT_DAGHERO_CNN_2LAYER_CONV2D_E05_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/no_accel_rotation_v2/daghero_cnn_2layer_conv2d/e05/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E05_daghero_cnn_2layer_conv2d_r0_qat.tflite`
- Model size: 26.73 KB
- Accuracy: 0.9931
- Macro-F1: 0.9906

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/off/daghero_cnn_2layer_conv2d/e05/confusion_off_qat_daghero_cnn_2layer_conv2d_e05_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9985, R=0.9949, F1=0.9967, support=2723
- Jogging: P=0.9948, R=0.9995, F1=0.9972, support=2109
- Upstairs: P=0.9754, R=0.9767, F1=0.9760, support=730
- Downstairs: P=0.9779, R=0.9779, F1=0.9779, support=587
- Sitting: P=1.0000, R=0.9948, F1=0.9974, support=381
- Standing: P=0.9967, R=1.0000, F1=0.9984, support=304
