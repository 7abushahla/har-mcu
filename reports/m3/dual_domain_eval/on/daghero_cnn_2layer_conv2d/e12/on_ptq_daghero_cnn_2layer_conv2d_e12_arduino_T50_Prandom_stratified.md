# ON_PTQ_DAGHERO_CNN_2LAYER_CONV2D_E12_ARDUINO TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/accel_rotation/daghero_cnn_2layer_conv2d/e12/daghero_cnn_2layer_conv2d_T50_Prandom_stratified_E12_daghero_cnn_2layer_conv2d_r0_ptq_int8.tflite`
- Model size: 26.13 KB
- Accuracy: 0.9707
- Macro-F1: 0.9705

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/daghero_cnn_2layer_conv2d/e12/confusion_on_ptq_daghero_cnn_2layer_conv2d_e12_arduino_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9832, R=0.9962, F1=0.9897, support=529
- Jogging: P=0.9775, R=0.9886, F1=0.9831, support=528
- Upstairs: P=0.9190, R=0.9225, F1=0.9208, support=529
- Downstairs: P=0.9472, R=0.9167, F1=0.9317, support=528
- Sitting: P=0.9981, R=1.0000, F1=0.9991, support=528
- Standing: P=0.9981, R=1.0000, F1=0.9991, support=528
