# ON_FP32_DAGHERO_CNN_2LAYER_CONV2D_E03_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E03_arduino_downsample_20hz_T100/accel_rotation/daghero_cnn_2layer_conv2d/e03/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E03_daghero_cnn_2layer_conv2d_r0_fp32.tflite`
- Model size: 80.41 KB
- Accuracy: 0.9821
- Macro-F1: 0.9688

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/daghero_cnn_2layer_conv2d/e03/confusion_on_fp32_daghero_cnn_2layer_conv2d_e03_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9959, R=0.9927, F1=0.9943, support=2723
- Jogging: P=0.9896, R=0.9934, F1=0.9915, support=2109
- Upstairs: P=0.9700, R=0.9301, F1=0.9497, support=730
- Downstairs: P=0.9338, R=0.9847, F1=0.9585, support=587
- Sitting: P=0.9682, R=0.9580, F1=0.9631, support=381
- Standing: P=0.9511, R=0.9605, F1=0.9558, support=304
