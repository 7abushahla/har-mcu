# OFF_QAT_DEEPCONV_LSTM_CONV2D_E05_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/no_accel_rotation_v2/deepconv_lstm_conv2d/e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.4994
- Macro-F1: 0.4883

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/off/deepconv_lstm_conv2d/e05/confusion_off_qat_deepconv_lstm_conv2d_e05_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.5089, R=0.6515, F1=0.5714, support=264
- Jogging: P=0.9286, R=0.2471, F1=0.3904, support=263
- Upstairs: P=0.3230, R=0.3144, F1=0.3186, support=264
- Downstairs: P=0.2265, R=0.3106, F1=0.2620, support=264
- Sitting: P=0.7333, R=1.0000, F1=0.8462, support=264
- Standing: P=0.6359, R=0.4715, F1=0.5415, support=263
