# ON_PTQ_DAGHERO_CNN_2LAYER_CONV2D_E09_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/accel_rotation_v3_target_clusters_p025/daghero_cnn_2layer_conv2d/e09/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E09_daghero_cnn_2layer_conv2d_r0_ptq_int8.tflite`
- Model size: 26.13 KB
- Accuracy: 0.9943
- Macro-F1: 0.9943

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/daghero_cnn_2layer_conv2d/e09/confusion_on_ptq_daghero_cnn_2layer_conv2d_e09_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=1.0000, R=1.0000, F1=1.0000, support=264
- Jogging: P=1.0000, R=0.9848, F1=0.9923, support=263
- Upstairs: P=0.9742, R=1.0000, F1=0.9869, support=264
- Downstairs: P=0.9923, R=0.9811, F1=0.9867, support=264
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=264
- Standing: P=1.0000, R=1.0000, F1=1.0000, support=263
