# ON_PTQ_DAGHERO_CNN_2LAYER_CONV2D_E08_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E08_T50_window/accel_rotation/daghero_cnn_2layer_conv2d/e08/daghero_cnn_2layer_conv2d_T50_Prandom_stratified_E08_daghero_cnn_2layer_conv2d_r0_ptq_int8.tflite`
- Model size: 26.13 KB
- Accuracy: 0.9762
- Macro-F1: 0.9646

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/daghero_cnn_2layer_conv2d/e08/confusion_on_ptq_daghero_cnn_2layer_conv2d_e08_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9882, R=0.9894, F1=0.9888, support=5482
- Jogging: P=0.9962, R=0.9889, F1=0.9926, support=4250
- Upstairs: P=0.9080, R=0.9416, F1=0.9245, support=1541
- Downstairs: P=0.9408, R=0.9167, F1=0.9286, support=1249
- Sitting: P=0.9882, R=0.9704, F1=0.9792, support=777
- Standing: P=0.9639, R=0.9840, F1=0.9738, support=624
