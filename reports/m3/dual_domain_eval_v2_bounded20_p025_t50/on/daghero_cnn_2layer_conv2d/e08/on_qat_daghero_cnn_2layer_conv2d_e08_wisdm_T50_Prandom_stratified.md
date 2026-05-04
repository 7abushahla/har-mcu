# ON_QAT_DAGHERO_CNN_2LAYER_CONV2D_E08_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E08_T50_window/accel_rotation_v2_bounded20_p025/daghero_cnn_2layer_conv2d/e08/daghero_cnn_2layer_conv2d_T50_Prandom_stratified_E08_daghero_cnn_2layer_conv2d_r0_qat.tflite`
- Model size: 26.73 KB
- Accuracy: 0.9879
- Macro-F1: 0.9837

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025_t50/on/daghero_cnn_2layer_conv2d/e08/confusion_on_qat_daghero_cnn_2layer_conv2d_e08_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9918, R=0.9949, F1=0.9934, support=5482
- Jogging: P=0.9951, R=0.9969, F1=0.9960, support=4250
- Upstairs: P=0.9641, R=0.9585, F1=0.9613, support=1541
- Downstairs: P=0.9659, R=0.9536, F1=0.9597, support=1249
- Sitting: P=0.9936, R=0.9936, F1=0.9936, support=777
- Standing: P=0.9984, R=0.9984, F1=0.9984, support=624
