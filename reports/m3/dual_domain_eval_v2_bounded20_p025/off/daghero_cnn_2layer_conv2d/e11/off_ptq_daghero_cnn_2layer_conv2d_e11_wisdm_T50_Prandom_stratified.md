# OFF_PTQ_DAGHERO_CNN_2LAYER_CONV2D_E11_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E11_wisdm_pretrain_arduino_finetune_T50/no_accel_rotation_v2/daghero_cnn_2layer_conv2d/e11/daghero_cnn_2layer_conv2d_T50_Prandom_stratified_E11_daghero_cnn_2layer_conv2d_r0_ptq_int8.tflite`
- Model size: 26.13 KB
- Accuracy: 0.3484
- Macro-F1: 0.2036

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/off/daghero_cnn_2layer_conv2d/e11/confusion_off_ptq_daghero_cnn_2layer_conv2d_e11_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.0164, R=0.0004, F1=0.0007, support=5482
- Jogging: P=0.3683, R=1.0000, F1=0.5384, support=4250
- Upstairs: P=0.1782, R=0.2213, F1=0.1974, support=1541
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=1249
- Sitting: P=0.8990, R=0.3320, F1=0.4850, support=777
- Standing: P=0.0000, R=0.0000, F1=0.0000, support=624
