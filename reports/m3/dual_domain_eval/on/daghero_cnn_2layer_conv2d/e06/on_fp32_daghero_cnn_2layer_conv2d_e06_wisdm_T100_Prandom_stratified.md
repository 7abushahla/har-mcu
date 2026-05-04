# ON_FP32_DAGHERO_CNN_2LAYER_CONV2D_E06_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E06_no_norm_matched/accel_rotation/daghero_cnn_2layer_conv2d/e06/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E06_daghero_cnn_2layer_conv2d_r0_fp32.tflite`
- Model size: 80.41 KB
- Accuracy: 0.9770
- Macro-F1: 0.9637

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/daghero_cnn_2layer_conv2d/e06/confusion_on_fp32_daghero_cnn_2layer_conv2d_e06_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9798, R=0.9963, F1=0.9880, support=2723
- Jogging: P=0.9914, R=0.9867, F1=0.9891, support=2109
- Upstairs: P=0.9489, R=0.9411, F1=0.9450, support=730
- Downstairs: P=0.9659, R=0.9182, F1=0.9415, support=587
- Sitting: P=0.9682, R=0.9580, F1=0.9631, support=381
- Standing: P=0.9511, R=0.9605, F1=0.9558, support=304
