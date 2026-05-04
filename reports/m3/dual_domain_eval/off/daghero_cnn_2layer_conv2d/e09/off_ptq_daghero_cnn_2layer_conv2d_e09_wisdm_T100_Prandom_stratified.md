# OFF_PTQ_DAGHERO_CNN_2LAYER_CONV2D_E09_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/no_accel_rotation/daghero_cnn_2layer_conv2d/e09/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E09_daghero_cnn_2layer_conv2d_r0_ptq_int8.tflite`
- Model size: 26.13 KB
- Accuracy: 0.3426
- Macro-F1: 0.1980

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/daghero_cnn_2layer_conv2d/e09/confusion_off_ptq_daghero_cnn_2layer_conv2d_e09_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.0000, R=0.0000, F1=0.0000, support=2723
- Jogging: P=0.3385, R=1.0000, F1=0.5058, support=2109
- Upstairs: P=0.2000, R=0.1219, F1=0.1515, support=730
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=587
- Sitting: P=0.9051, R=0.3753, F1=0.5306, support=381
- Standing: P=0.0000, R=0.0000, F1=0.0000, support=304
