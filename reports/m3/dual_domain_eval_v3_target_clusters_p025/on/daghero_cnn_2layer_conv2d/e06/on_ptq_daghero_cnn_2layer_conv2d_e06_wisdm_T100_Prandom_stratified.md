# ON_PTQ_DAGHERO_CNN_2LAYER_CONV2D_E06_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E06_no_norm_matched/accel_rotation_v3_target_clusters_p025/daghero_cnn_2layer_conv2d/e06/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E06_daghero_cnn_2layer_conv2d_r0_ptq_int8.tflite`
- Model size: 26.13 KB
- Accuracy: 0.9892
- Macro-F1: 0.9807

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/daghero_cnn_2layer_conv2d/e06/confusion_on_ptq_daghero_cnn_2layer_conv2d_e06_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9993, R=0.9927, F1=0.9959, support=2723
- Jogging: P=0.9929, R=0.9995, F1=0.9962, support=2109
- Upstairs: P=0.9725, R=0.9699, F1=0.9712, support=730
- Downstairs: P=0.9663, R=0.9779, F1=0.9721, support=587
- Sitting: P=0.9946, R=0.9580, F1=0.9759, support=381
- Standing: P=0.9527, R=0.9934, F1=0.9726, support=304
