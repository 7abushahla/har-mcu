# ON_FP32_DAGHERO_CNN_2LAYER_CONV2D_E04_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/accel_rotation/daghero_cnn_2layer_conv2d/e04/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E04_daghero_cnn_2layer_conv2d_r0_fp32.tflite`
- Model size: 80.41 KB
- Accuracy: 0.9813
- Macro-F1: 0.9676

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/daghero_cnn_2layer_conv2d/e04/confusion_on_fp32_daghero_cnn_2layer_conv2d_e04_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9945, R=0.9930, F1=0.9938, support=2723
- Jogging: P=0.9896, R=0.9919, F1=0.9908, support=2109
- Upstairs: P=0.9685, R=0.9274, F1=0.9475, support=730
- Downstairs: P=0.9337, R=0.9830, F1=0.9577, support=587
- Sitting: P=0.9656, R=0.9580, F1=0.9618, support=381
- Standing: P=0.9510, R=0.9572, F1=0.9541, support=304
