# ON_PTQ_DAGHERO_CNN_2LAYER_CONV2D_E03_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E03_arduino_downsample_20hz_T100/accel_rotation/daghero_cnn_2layer_conv2d/e03/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E03_daghero_cnn_2layer_conv2d_r0_ptq_int8.tflite`
- Model size: 26.13 KB
- Accuracy: 0.9819
- Macro-F1: 0.9671

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/daghero_cnn_2layer_conv2d/e03/confusion_on_ptq_daghero_cnn_2layer_conv2d_e03_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9941, R=0.9934, F1=0.9938, support=2723
- Jogging: P=0.9896, R=0.9943, F1=0.9920, support=2109
- Upstairs: P=0.9729, R=0.9329, F1=0.9524, support=730
- Downstairs: P=0.9426, R=0.9796, F1=0.9607, support=587
- Sitting: P=0.9555, R=0.9580, F1=0.9567, support=381
- Standing: P=0.9503, R=0.9441, F1=0.9472, support=304
