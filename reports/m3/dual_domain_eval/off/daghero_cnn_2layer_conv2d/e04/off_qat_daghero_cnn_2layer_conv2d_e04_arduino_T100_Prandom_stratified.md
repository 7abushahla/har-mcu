# OFF_QAT_DAGHERO_CNN_2LAYER_CONV2D_E04_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/no_accel_rotation/daghero_cnn_2layer_conv2d/e04/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E04_daghero_cnn_2layer_conv2d_r0_qat.tflite`
- Model size: 26.73 KB
- Accuracy: 0.5120
- Macro-F1: 0.4521

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/daghero_cnn_2layer_conv2d/e04/confusion_off_qat_daghero_cnn_2layer_conv2d_e04_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.7500, R=0.0455, F1=0.0857, support=264
- Jogging: P=1.0000, R=0.5247, F1=0.6883, support=263
- Upstairs: P=0.2919, R=0.9886, F1=0.4508, support=264
- Downstairs: P=0.3333, R=0.0076, F1=0.0148, support=264
- Sitting: P=0.6684, R=1.0000, F1=0.8012, support=264
- Standing: P=1.0000, R=0.5057, F1=0.6717, support=263
