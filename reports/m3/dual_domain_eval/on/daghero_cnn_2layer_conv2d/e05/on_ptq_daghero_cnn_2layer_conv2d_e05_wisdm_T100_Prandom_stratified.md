# ON_PTQ_DAGHERO_CNN_2LAYER_CONV2D_E05_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/accel_rotation/daghero_cnn_2layer_conv2d/e05/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E05_daghero_cnn_2layer_conv2d_r0_ptq_int8.tflite`
- Model size: 26.13 KB
- Accuracy: 0.9823
- Macro-F1: 0.9689

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/daghero_cnn_2layer_conv2d/e05/confusion_on_ptq_daghero_cnn_2layer_conv2d_e05_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9941, R=0.9927, F1=0.9934, support=2723
- Jogging: P=0.9891, R=0.9938, F1=0.9915, support=2109
- Upstairs: P=0.9622, R=0.9425, F1=0.9522, support=730
- Downstairs: P=0.9581, R=0.9744, F1=0.9662, support=587
- Sitting: P=0.9605, R=0.9580, F1=0.9593, support=381
- Standing: P=0.9507, R=0.9507, F1=0.9507, support=304
