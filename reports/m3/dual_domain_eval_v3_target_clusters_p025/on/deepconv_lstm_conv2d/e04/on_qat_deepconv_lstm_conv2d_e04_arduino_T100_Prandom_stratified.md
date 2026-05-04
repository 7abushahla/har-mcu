# ON_QAT_DEEPCONV_LSTM_CONV2D_E04_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.4273
- Macro-F1: 0.4243

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/deepconv_lstm_conv2d/e04/confusion_on_qat_deepconv_lstm_conv2d_e04_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.3002, R=0.6061, F1=0.4015, support=264
- Jogging: P=0.8037, R=0.4981, F1=0.6150, support=263
- Upstairs: P=0.2968, R=0.3485, F1=0.3206, support=264
- Downstairs: P=0.0750, R=0.0341, F1=0.0469, support=264
- Sitting: P=0.5157, R=0.6212, F1=0.5636, support=264
- Standing: P=0.8696, R=0.4563, F1=0.5985, support=263
