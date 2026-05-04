# ON_FP32_DAGHERO_CNN_2LAYER_CONV2D_E10_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E10_arduino_from_scratch/accel_rotation/daghero_cnn_2layer_conv2d/e10/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E10_daghero_cnn_2layer_conv2d_r0_fp32.tflite`
- Model size: 80.41 KB
- Accuracy: 0.3093
- Macro-F1: 0.0863

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/daghero_cnn_2layer_conv2d/e10/confusion_on_fp32_daghero_cnn_2layer_conv2d_e10_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.0000, R=0.0000, F1=0.0000, support=2723
- Jogging: P=0.3428, R=1.0000, F1=0.5106, support=2109
- Upstairs: P=0.0073, R=0.0068, F1=0.0071, support=730
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=587
- Sitting: P=0.0000, R=0.0000, F1=0.0000, support=381
- Standing: P=0.0000, R=0.0000, F1=0.0000, support=304
