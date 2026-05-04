# ON_QAT_DAGHERO_CNN_2LAYER_CONV2D_E06_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E06_no_norm_matched/accel_rotation_v3_target_clusters_p025/daghero_cnn_2layer_conv2d/e06/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E06_daghero_cnn_2layer_conv2d_r0_qat.tflite`
- Model size: 26.73 KB
- Accuracy: 0.9893
- Macro-F1: 0.9812

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/daghero_cnn_2layer_conv2d/e06/confusion_on_qat_daghero_cnn_2layer_conv2d_e06_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9971, R=0.9949, F1=0.9960, support=2723
- Jogging: P=0.9934, R=0.9986, F1=0.9960, support=2109
- Upstairs: P=0.9713, R=0.9726, F1=0.9719, support=730
- Downstairs: P=0.9759, R=0.9676, F1=0.9718, support=587
- Sitting: P=0.9973, R=0.9580, F1=0.9772, support=381
- Standing: P=0.9528, R=0.9967, F1=0.9743, support=304
