# OFF_FP32_DEEPCONV_LSTM_CONV2D_E05_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/no_accel_rotation_v2/deepconv_lstm_conv2d/e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.5386
- Macro-F1: 0.5522

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/off/deepconv_lstm_conv2d/e05/confusion_off_fp32_deepconv_lstm_conv2d_e05_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.3653, R=0.6061, F1=0.4558, support=264
- Jogging: P=0.9930, R=0.5361, F1=0.6963, support=263
- Upstairs: P=0.3176, R=0.3561, F1=0.3357, support=264
- Downstairs: P=0.2426, R=0.2500, F1=0.2463, support=264
- Sitting: P=0.9362, R=1.0000, F1=0.9670, support=264
- Standing: P=0.8355, R=0.4829, F1=0.6120, support=263
