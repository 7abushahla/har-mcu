# OFF_PTQ_DAGHERO_CNN_2LAYER_CONV2D_E08_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E08_T50_window/no_accel_rotation_v2/daghero_cnn_2layer_conv2d/e08/daghero_cnn_2layer_conv2d_T50_Prandom_stratified_E08_daghero_cnn_2layer_conv2d_r0_ptq_int8.tflite`
- Model size: 26.13 KB
- Accuracy: 0.9867
- Macro-F1: 0.9817

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025_t50/off/daghero_cnn_2layer_conv2d/e08/confusion_off_ptq_daghero_cnn_2layer_conv2d_e08_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9951, R=0.9940, F1=0.9945, support=5482
- Jogging: P=0.9909, R=0.9974, F1=0.9941, support=4250
- Upstairs: P=0.9675, R=0.9468, F1=0.9570, support=1541
- Downstairs: P=0.9493, R=0.9592, F1=0.9542, support=1249
- Sitting: P=0.9936, R=0.9936, F1=0.9936, support=777
- Standing: P=0.9984, R=0.9952, F1=0.9968, support=624
