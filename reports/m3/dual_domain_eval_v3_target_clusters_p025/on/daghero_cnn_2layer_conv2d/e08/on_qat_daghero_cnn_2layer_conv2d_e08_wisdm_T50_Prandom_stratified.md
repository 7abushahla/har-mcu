# ON_QAT_DAGHERO_CNN_2LAYER_CONV2D_E08_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E08_T50_window/accel_rotation_v3_target_clusters_p025/daghero_cnn_2layer_conv2d/e08/daghero_cnn_2layer_conv2d_T50_Prandom_stratified_E08_daghero_cnn_2layer_conv2d_r0_qat.tflite`
- Model size: 26.73 KB
- Accuracy: 0.9848
- Macro-F1: 0.9792

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/daghero_cnn_2layer_conv2d/e08/confusion_on_qat_daghero_cnn_2layer_conv2d_e08_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9907, R=0.9940, F1=0.9924, support=5482
- Jogging: P=0.9948, R=0.9955, F1=0.9952, support=4250
- Upstairs: P=0.9467, R=0.9565, F1=0.9516, support=1541
- Downstairs: P=0.9596, R=0.9319, F1=0.9456, support=1249
- Sitting: P=0.9987, R=0.9936, F1=0.9961, support=777
- Standing: P=0.9920, R=0.9968, F1=0.9944, support=624
