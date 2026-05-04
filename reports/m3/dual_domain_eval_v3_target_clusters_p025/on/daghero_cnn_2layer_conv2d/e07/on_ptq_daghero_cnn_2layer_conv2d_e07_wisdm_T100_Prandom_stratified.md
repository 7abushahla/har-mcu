# ON_PTQ_DAGHERO_CNN_2LAYER_CONV2D_E07_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E07_skip_inference_norm_diag/accel_rotation_v3_target_clusters_p025/daghero_cnn_2layer_conv2d/e07/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E07_daghero_cnn_2layer_conv2d_r0_ptq_int8.tflite`
- Model size: 26.13 KB
- Accuracy: 0.9908
- Macro-F1: 0.9834

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/daghero_cnn_2layer_conv2d/e07/confusion_on_ptq_daghero_cnn_2layer_conv2d_e07_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=1.0000, R=0.9934, F1=0.9967, support=2723
- Jogging: P=0.9948, R=1.0000, F1=0.9974, support=2109
- Upstairs: P=0.9700, R=0.9740, F1=0.9720, support=730
- Downstairs: P=0.9730, R=0.9813, F1=0.9771, support=587
- Sitting: P=0.9973, R=0.9633, F1=0.9800, support=381
- Standing: P=0.9589, R=0.9967, F1=0.9774, support=304
