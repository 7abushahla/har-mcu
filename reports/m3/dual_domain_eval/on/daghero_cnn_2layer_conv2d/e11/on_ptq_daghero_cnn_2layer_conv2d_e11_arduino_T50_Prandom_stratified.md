# ON_PTQ_DAGHERO_CNN_2LAYER_CONV2D_E11_ARDUINO TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E11_wisdm_pretrain_arduino_finetune_T50/accel_rotation/daghero_cnn_2layer_conv2d/e11/daghero_cnn_2layer_conv2d_T50_Prandom_stratified_E11_daghero_cnn_2layer_conv2d_r0_ptq_int8.tflite`
- Model size: 26.13 KB
- Accuracy: 0.9726
- Macro-F1: 0.9724

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/daghero_cnn_2layer_conv2d/e11/confusion_on_ptq_daghero_cnn_2layer_conv2d_e11_arduino_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9635, R=0.9981, F1=0.9805, support=529
- Jogging: P=0.9776, R=0.9924, F1=0.9850, support=528
- Upstairs: P=0.9388, R=0.9282, F1=0.9335, support=529
- Downstairs: P=0.9585, R=0.9186, F1=0.9381, support=528
- Sitting: P=0.9981, R=0.9981, F1=0.9981, support=528
- Standing: P=0.9981, R=1.0000, F1=0.9991, support=528
