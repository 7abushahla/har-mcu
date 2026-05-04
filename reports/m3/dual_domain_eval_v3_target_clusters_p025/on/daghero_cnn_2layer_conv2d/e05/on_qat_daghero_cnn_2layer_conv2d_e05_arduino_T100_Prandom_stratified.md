# ON_QAT_DAGHERO_CNN_2LAYER_CONV2D_E05_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/accel_rotation_v3_target_clusters_p025/daghero_cnn_2layer_conv2d/e05/daghero_cnn_2layer_conv2d_T100_Prandom_stratified_E05_daghero_cnn_2layer_conv2d_r0_qat.tflite`
- Model size: 26.73 KB
- Accuracy: 0.5499
- Macro-F1: 0.5136

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 6
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'MAX_POOL_2D', 'MEAN', 'RESHAPE', 'SOFTMAX']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/daghero_cnn_2layer_conv2d/e05/confusion_on_qat_daghero_cnn_2layer_conv2d_e05_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.5606, R=0.2803, F1=0.3737, support=264
- Jogging: P=1.0000, R=0.5475, F1=0.7076, support=263
- Upstairs: P=0.3102, R=0.9129, F1=0.4630, support=264
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=264
- Sitting: P=0.6947, R=1.0000, F1=0.8199, support=264
- Standing: P=1.0000, R=0.5589, F1=0.7171, support=263
