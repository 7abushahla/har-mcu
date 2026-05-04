# ON_PTQ_DAGHERO_CNN_2LAYER_CONV2D_E05_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/accel_rotation_v3_target_clusters_p025/daghero_cnn_2layer_conv2d/e05/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E05_daghero_cnn_2layer_conv2d_r0_ptq_int8.tflite`
- Model size: 26.13 KB
- Accuracy: 0.9911
- Macro-F1: 0.9875

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/daghero_cnn_2layer_conv2d/e05/confusion_on_ptq_daghero_cnn_2layer_conv2d_e05_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=1.0000, R=0.9905, F1=0.9952, support=2723
- Jogging: P=0.9943, R=0.9995, F1=0.9969, support=2109
- Upstairs: P=0.9635, R=0.9753, F1=0.9694, support=730
- Downstairs: P=0.9680, R=0.9796, F1=0.9738, support=587
- Sitting: P=0.9974, R=0.9921, F1=0.9947, support=381
- Standing: P=0.9934, R=0.9967, F1=0.9951, support=304
