# ON_FP32_DAGHERO_CNN_2LAYER_CONV2D_E00_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/accel_rotation/daghero_cnn_2layer_conv2d/e00/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E00_daghero_cnn_2layer_conv2d_r0_fp32.tflite`
- Model size: 80.41 KB
- Accuracy: 0.9785
- Macro-F1: 0.9664

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/daghero_cnn_2layer_conv2d/e00/confusion_on_fp32_daghero_cnn_2layer_conv2d_e00_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9830, R=0.9956, F1=0.9892, support=2723
- Jogging: P=0.9914, R=0.9872, F1=0.9893, support=2109
- Upstairs: P=0.9510, R=0.9301, F1=0.9404, support=730
- Downstairs: P=0.9619, R=0.9472, F1=0.9545, support=587
- Sitting: P=0.9733, R=0.9580, F1=0.9656, support=381
- Standing: P=0.9515, R=0.9671, F1=0.9592, support=304
