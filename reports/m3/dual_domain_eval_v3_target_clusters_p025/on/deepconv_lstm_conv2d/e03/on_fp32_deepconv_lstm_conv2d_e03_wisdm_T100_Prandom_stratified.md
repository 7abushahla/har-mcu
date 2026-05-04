# ON_FP32_DEEPCONV_LSTM_CONV2D_E03_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E03_arduino_downsample_20hz_T100/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e03/deepconv_lstm_conv2d_T100_Prandom_stratified_E03_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.9821
- Macro-F1: 0.9716

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/deepconv_lstm_conv2d/e03/confusion_on_fp32_deepconv_lstm_conv2d_e03_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9960, R=0.9938, F1=0.9949, support=2723
- Jogging: P=0.9924, R=0.9953, F1=0.9938, support=2109
- Upstairs: P=0.9066, R=0.9712, F1=0.9378, support=730
- Downstairs: P=0.9776, R=0.8910, F1=0.9323, support=587
- Sitting: P=0.9868, R=0.9843, F1=0.9855, support=381
- Standing: P=0.9836, R=0.9868, F1=0.9852, support=304
