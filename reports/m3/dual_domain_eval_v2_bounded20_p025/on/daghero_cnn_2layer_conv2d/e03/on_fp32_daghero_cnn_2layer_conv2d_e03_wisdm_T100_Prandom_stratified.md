# ON_FP32_DAGHERO_CNN_2LAYER_CONV2D_E03_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E03_arduino_downsample_20hz_T100/accel_rotation_v2_bounded20_p025/daghero_cnn_2layer_conv2d/e03/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E03_daghero_cnn_2layer_conv2d_r0_fp32.tflite`
- Model size: 80.41 KB
- Accuracy: 0.9906
- Macro-F1: 0.9828

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/on/daghero_cnn_2layer_conv2d/e03/confusion_on_fp32_daghero_cnn_2layer_conv2d_e03_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9993, R=0.9938, F1=0.9965, support=2723
- Jogging: P=0.9967, R=0.9991, F1=0.9979, support=2109
- Upstairs: P=0.9625, R=0.9836, F1=0.9729, support=730
- Downstairs: P=0.9794, R=0.9710, F1=0.9752, support=587
- Sitting: P=1.0000, R=0.9580, F1=0.9786, support=381
- Standing: P=0.9530, R=1.0000, F1=0.9759, support=304
