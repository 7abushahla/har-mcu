# ON_QAT_DAGHERO_CNN_2LAYER_CONV2D_E07_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E07_skip_inference_norm_diag/accel_rotation_v3_target_clusters_p025/daghero_cnn_2layer_conv2d/e07/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E07_daghero_cnn_2layer_conv2d_r0_qat.tflite`
- Model size: 26.73 KB
- Accuracy: 0.9906
- Macro-F1: 0.9826

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/daghero_cnn_2layer_conv2d/e07/confusion_on_qat_daghero_cnn_2layer_conv2d_e07_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9974, R=0.9956, F1=0.9965, support=2723
- Jogging: P=0.9953, R=0.9995, F1=0.9974, support=2109
- Upstairs: P=0.9767, R=0.9767, F1=0.9767, support=730
- Downstairs: P=0.9760, R=0.9710, F1=0.9735, support=587
- Sitting: P=0.9973, R=0.9580, F1=0.9772, support=381
- Standing: P=0.9528, R=0.9967, F1=0.9743, support=304
