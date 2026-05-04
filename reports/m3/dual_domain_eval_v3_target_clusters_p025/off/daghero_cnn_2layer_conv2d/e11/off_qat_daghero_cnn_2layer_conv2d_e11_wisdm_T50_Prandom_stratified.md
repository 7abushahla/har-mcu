# OFF_QAT_DAGHERO_CNN_2LAYER_CONV2D_E11_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E11_wisdm_pretrain_arduino_finetune_T50/no_accel_rotation_v2/daghero_cnn_2layer_conv2d/e11/daghero_cnn_2layer_conv2d_T50_Prandom_stratified_E11_daghero_cnn_2layer_conv2d_r0_qat.tflite`
- Model size: 26.73 KB
- Accuracy: 0.3506
- Macro-F1: 0.2229

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/off/daghero_cnn_2layer_conv2d/e11/confusion_off_qat_daghero_cnn_2layer_conv2d_e11_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.0119, R=0.0002, F1=0.0004, support=5482
- Jogging: P=0.3543, R=1.0000, F1=0.5232, support=4250
- Upstairs: P=0.1601, R=0.1441, F1=0.1516, support=1541
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=1249
- Sitting: P=0.8967, R=0.5251, F1=0.6623, support=777
- Standing: P=0.0000, R=0.0000, F1=0.0000, support=624
