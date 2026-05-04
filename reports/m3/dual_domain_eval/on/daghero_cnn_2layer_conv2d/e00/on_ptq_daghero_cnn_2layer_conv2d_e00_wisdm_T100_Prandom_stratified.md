# ON_PTQ_DAGHERO_CNN_2LAYER_CONV2D_E00_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/accel_rotation/daghero_cnn_2layer_conv2d/e00/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E00_daghero_cnn_2layer_conv2d_r0_ptq_int8.tflite`
- Model size: 26.13 KB
- Accuracy: 0.9769
- Macro-F1: 0.9636

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/daghero_cnn_2layer_conv2d/e00/confusion_on_ptq_daghero_cnn_2layer_conv2d_e00_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9798, R=0.9956, F1=0.9876, support=2723
- Jogging: P=0.9919, R=0.9877, F1=0.9898, support=2109
- Upstairs: P=0.9471, R=0.9315, F1=0.9392, support=730
- Downstairs: P=0.9646, R=0.9284, F1=0.9462, support=587
- Sitting: P=0.9682, R=0.9580, F1=0.9631, support=381
- Standing: P=0.9511, R=0.9605, F1=0.9558, support=304
