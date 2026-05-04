# OFF_PTQ_DAGHERO_CNN_2LAYER_CONV2D_E12_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/no_accel_rotation/daghero_cnn_2layer_conv2d/e12/daghero_cnn_2layer_conv2d_T50_Prandom_stratified_E12_daghero_cnn_2layer_conv2d_r0_ptq_int8.tflite`
- Model size: 26.13 KB
- Accuracy: 0.3297
- Macro-F1: 0.1538

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/daghero_cnn_2layer_conv2d/e12/confusion_off_ptq_daghero_cnn_2layer_conv2d_e12_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.0000, R=0.0000, F1=0.0000, support=5482
- Jogging: P=0.3370, R=0.9953, F1=0.5035, support=4250
- Upstairs: P=0.2024, R=0.1655, F1=0.1821, support=1541
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=1249
- Sitting: P=0.9722, R=0.1351, F1=0.2373, support=777
- Standing: P=0.0000, R=0.0000, F1=0.0000, support=624
