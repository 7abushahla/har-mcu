# ON_QAT_DAGHERO_CNN_2LAYER_CONV2D_E06_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E06_no_norm_matched/accel_rotation/daghero_cnn_2layer_conv2d/e06/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E06_daghero_cnn_2layer_conv2d_r0_qat.tflite`
- Model size: 26.73 KB
- Accuracy: 0.9848
- Macro-F1: 0.9749

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/daghero_cnn_2layer_conv2d/e06/confusion_on_qat_daghero_cnn_2layer_conv2d_e06_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9916, R=0.9949, F1=0.9932, support=2723
- Jogging: P=0.9938, R=0.9943, F1=0.9941, support=2109
- Upstairs: P=0.9651, R=0.9466, F1=0.9557, support=730
- Downstairs: P=0.9595, R=0.9676, F1=0.9635, support=587
- Sitting: P=0.9892, R=0.9580, F1=0.9733, support=381
- Standing: P=0.9524, R=0.9868, F1=0.9693, support=304
