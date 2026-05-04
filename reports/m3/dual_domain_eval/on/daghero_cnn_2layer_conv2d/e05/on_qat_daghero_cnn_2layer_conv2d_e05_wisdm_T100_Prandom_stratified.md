# ON_QAT_DAGHERO_CNN_2LAYER_CONV2D_E05_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/accel_rotation/daghero_cnn_2layer_conv2d/e05/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E05_daghero_cnn_2layer_conv2d_r0_qat.tflite`
- Model size: 26.73 KB
- Accuracy: 0.9858
- Macro-F1: 0.9775

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/daghero_cnn_2layer_conv2d/e05/confusion_on_qat_daghero_cnn_2layer_conv2d_e05_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9927, R=0.9949, F1=0.9938, support=2723
- Jogging: P=0.9920, R=0.9943, F1=0.9931, support=2109
- Upstairs: P=0.9718, R=0.9438, F1=0.9576, support=730
- Downstairs: P=0.9599, R=0.9779, F1=0.9688, support=587
- Sitting: P=0.9973, R=0.9580, F1=0.9772, support=381
- Standing: P=0.9528, R=0.9967, F1=0.9743, support=304
