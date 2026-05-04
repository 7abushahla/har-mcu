# ON_FP32_DAGHERO_CNN_2LAYER_CONV2D_E07_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E07_skip_inference_norm_diag/accel_rotation/daghero_cnn_2layer_conv2d/e07/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E07_daghero_cnn_2layer_conv2d_r0_fp32.tflite`
- Model size: 80.41 KB
- Accuracy: 0.9763
- Macro-F1: 0.9633

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/daghero_cnn_2layer_conv2d/e07/confusion_on_fp32_daghero_cnn_2layer_conv2d_e07_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9794, R=0.9960, F1=0.9876, support=2723
- Jogging: P=0.9924, R=0.9848, F1=0.9886, support=2109
- Upstairs: P=0.9494, R=0.9260, F1=0.9376, support=730
- Downstairs: P=0.9531, R=0.9353, F1=0.9441, support=587
- Sitting: P=0.9707, R=0.9580, F1=0.9643, support=381
- Standing: P=0.9513, R=0.9638, F1=0.9575, support=304
