# ON_PTQ_DAGHERO_CNN_2LAYER_CONV2D_E03_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E03_arduino_downsample_20hz_T100/accel_rotation_v2_bounded20_p025/daghero_cnn_2layer_conv2d/e03/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E03_daghero_cnn_2layer_conv2d_r0_ptq_int8.tflite`
- Model size: 26.13 KB
- Accuracy: 0.9920
- Macro-F1: 0.9877

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/on/daghero_cnn_2layer_conv2d/e03/confusion_on_ptq_daghero_cnn_2layer_conv2d_e03_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9989, R=0.9938, F1=0.9963, support=2723
- Jogging: P=0.9962, R=0.9991, F1=0.9976, support=2109
- Upstairs: P=0.9612, R=0.9849, F1=0.9729, support=730
- Downstairs: P=0.9827, R=0.9676, F1=0.9751, support=587
- Sitting: P=1.0000, R=0.9843, F1=0.9921, support=381
- Standing: P=0.9838, R=1.0000, F1=0.9918, support=304
