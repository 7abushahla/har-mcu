# ON_PTQ_DAGHERO_CNN_2LAYER_CONV2D_E06_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E06_no_norm_matched/accel_rotation/daghero_cnn_2layer_conv2d/e06/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E06_daghero_cnn_2layer_conv2d_r0_ptq_int8.tflite`
- Model size: 26.13 KB
- Accuracy: 0.9741
- Macro-F1: 0.9593

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/daghero_cnn_2layer_conv2d/e06/confusion_on_ptq_daghero_cnn_2layer_conv2d_e06_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9770, R=0.9967, F1=0.9867, support=2723
- Jogging: P=0.9919, R=0.9853, F1=0.9886, support=2109
- Upstairs: P=0.9260, R=0.9425, F1=0.9341, support=730
- Downstairs: P=0.9738, R=0.8859, F1=0.9277, support=587
- Sitting: P=0.9682, R=0.9580, F1=0.9631, support=381
- Standing: P=0.9511, R=0.9605, F1=0.9558, support=304
