# ON_QAT_DAGHERO_CNN_2LAYER_CONV2D_E08_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E08_T50_window/accel_rotation/daghero_cnn_2layer_conv2d/e08/daghero_cnn_2layer_conv2d_T50_Prandom_stratified_E08_daghero_cnn_2layer_conv2d_r0_qat.tflite`
- Model size: 26.73 KB
- Accuracy: 0.9767
- Macro-F1: 0.9666

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/daghero_cnn_2layer_conv2d/e08/confusion_on_qat_daghero_cnn_2layer_conv2d_e08_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9825, R=0.9931, F1=0.9878, support=5482
- Jogging: P=0.9941, R=0.9904, F1=0.9922, support=4250
- Upstairs: P=0.9147, R=0.9390, F1=0.9267, support=1541
- Downstairs: P=0.9631, R=0.8991, F1=0.9300, support=1249
- Sitting: P=0.9974, R=0.9704, F1=0.9837, support=777
- Standing: P=0.9643, R=0.9952, F1=0.9795, support=624
