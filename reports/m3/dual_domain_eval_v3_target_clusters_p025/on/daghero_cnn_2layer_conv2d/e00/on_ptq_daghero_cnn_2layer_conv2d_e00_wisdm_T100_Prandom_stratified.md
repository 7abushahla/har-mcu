# ON_PTQ_DAGHERO_CNN_2LAYER_CONV2D_E00_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/accel_rotation_v3_target_clusters_p025/daghero_cnn_2layer_conv2d/e00/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E00_daghero_cnn_2layer_conv2d_r0_ptq_int8.tflite`
- Model size: 26.13 KB
- Accuracy: 0.9881
- Macro-F1: 0.9799

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/daghero_cnn_2layer_conv2d/e00/confusion_on_ptq_daghero_cnn_2layer_conv2d_e00_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=1.0000, R=0.9893, F1=0.9946, support=2723
- Jogging: P=0.9934, R=0.9995, F1=0.9965, support=2109
- Upstairs: P=0.9594, R=0.9712, F1=0.9653, support=730
- Downstairs: P=0.9647, R=0.9779, F1=0.9712, support=587
- Sitting: P=0.9973, R=0.9580, F1=0.9772, support=381
- Standing: P=0.9528, R=0.9967, F1=0.9743, support=304
