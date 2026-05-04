# OFF_QAT_DAGHERO_CNN_2LAYER_CONV2D_E09_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/no_accel_rotation_v2/daghero_cnn_2layer_conv2d/e09/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E09_daghero_cnn_2layer_conv2d_r0_qat.tflite`
- Model size: 26.73 KB
- Accuracy: 0.3167
- Macro-F1: 0.0976

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/off/daghero_cnn_2layer_conv2d/e09/confusion_off_qat_daghero_cnn_2layer_conv2d_e09_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.1429, R=0.0055, F1=0.0106, support=2723
- Jogging: P=0.3296, R=1.0000, F1=0.4958, support=2109
- Upstairs: P=0.1189, R=0.0534, F1=0.0737, support=730
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=587
- Sitting: P=1.0000, R=0.0026, F1=0.0052, support=381
- Standing: P=0.0000, R=0.0000, F1=0.0000, support=304
