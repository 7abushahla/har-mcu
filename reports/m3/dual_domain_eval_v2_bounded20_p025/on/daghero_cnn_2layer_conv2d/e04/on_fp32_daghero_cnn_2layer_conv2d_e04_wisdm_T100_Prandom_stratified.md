# ON_FP32_DAGHERO_CNN_2LAYER_CONV2D_E04_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/accel_rotation_v2_bounded20_p025/daghero_cnn_2layer_conv2d/e04/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E04_daghero_cnn_2layer_conv2d_r0_fp32.tflite`
- Model size: 80.41 KB
- Accuracy: 0.9930
- Macro-F1: 0.9890

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/on/daghero_cnn_2layer_conv2d/e04/confusion_on_fp32_daghero_cnn_2layer_conv2d_e04_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9996, R=0.9945, F1=0.9971, support=2723
- Jogging: P=0.9962, R=0.9991, F1=0.9976, support=2109
- Upstairs: P=0.9728, R=0.9808, F1=0.9768, support=730
- Downstairs: P=0.9763, R=0.9813, F1=0.9788, support=587
- Sitting: P=1.0000, R=0.9843, F1=0.9921, support=381
- Standing: P=0.9838, R=1.0000, F1=0.9918, support=304
