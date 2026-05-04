# ON_PTQ_DAGHERO_CNN_2LAYER_CONV2D_E11_ARDUINO TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E11_wisdm_pretrain_arduino_finetune_T50/accel_rotation_v2_bounded20_p025/daghero_cnn_2layer_conv2d/e11/daghero_cnn_2layer_conv2d_T50_Prandom_stratified_E11_daghero_cnn_2layer_conv2d_r0_ptq_int8.tflite`
- Model size: 26.13 KB
- Accuracy: 0.9849
- Macro-F1: 0.9849

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/on/daghero_cnn_2layer_conv2d/e11/confusion_on_ptq_daghero_cnn_2layer_conv2d_e11_arduino_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9925, R=0.9981, F1=0.9953, support=529
- Jogging: P=0.9924, R=0.9905, F1=0.9915, support=528
- Upstairs: P=0.9585, R=0.9603, F1=0.9594, support=529
- Downstairs: P=0.9657, R=0.9602, F1=0.9630, support=528
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=528
- Standing: P=1.0000, R=1.0000, F1=1.0000, support=528
