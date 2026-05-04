# ON_PTQ_DAGHERO_CNN_2LAYER_CONV2D_E10_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E10_arduino_from_scratch/accel_rotation/daghero_cnn_2layer_conv2d/e10/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E10_daghero_cnn_2layer_conv2d_r0_ptq_int8.tflite`
- Model size: 26.13 KB
- Accuracy: 0.9829
- Macro-F1: 0.9829

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/daghero_cnn_2layer_conv2d/e10/confusion_on_ptq_daghero_cnn_2layer_conv2d_e10_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9778, R=1.0000, F1=0.9888, support=264
- Jogging: P=0.9923, R=0.9848, F1=0.9885, support=263
- Upstairs: P=0.9765, R=0.9432, F1=0.9595, support=264
- Downstairs: P=0.9517, R=0.9697, F1=0.9606, support=264
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=264
- Standing: P=1.0000, R=1.0000, F1=1.0000, support=263
