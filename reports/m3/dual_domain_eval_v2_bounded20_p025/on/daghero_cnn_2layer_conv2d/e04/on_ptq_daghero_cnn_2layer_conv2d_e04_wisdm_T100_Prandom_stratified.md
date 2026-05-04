# ON_PTQ_DAGHERO_CNN_2LAYER_CONV2D_E04_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/accel_rotation_v2_bounded20_p025/daghero_cnn_2layer_conv2d/e04/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E04_daghero_cnn_2layer_conv2d_r0_ptq_int8.tflite`
- Model size: 26.13 KB
- Accuracy: 0.9933
- Macro-F1: 0.9903

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/on/daghero_cnn_2layer_conv2d/e04/confusion_on_ptq_daghero_cnn_2layer_conv2d_e04_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9993, R=0.9945, F1=0.9969, support=2723
- Jogging: P=0.9967, R=0.9991, F1=0.9979, support=2109
- Upstairs: P=0.9702, R=0.9822, F1=0.9762, support=730
- Downstairs: P=0.9779, R=0.9779, F1=0.9779, support=587
- Sitting: P=1.0000, R=0.9921, F1=0.9960, support=381
- Standing: P=0.9935, R=1.0000, F1=0.9967, support=304
