# ON_FP32_DEEPCONV_LSTM_CONV2D_E04_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.5411
- Macro-F1: 0.4685

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/deepconv_lstm_conv2d/e04/confusion_on_fp32_deepconv_lstm_conv2d_e04_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.3333, R=0.0379, F1=0.0680, support=264
- Jogging: P=0.8417, R=0.7681, F1=0.8032, support=263
- Upstairs: P=0.3265, R=0.9015, F1=0.4794, support=264
- Downstairs: P=0.2222, R=0.0076, F1=0.0147, support=264
- Sitting: P=0.6247, R=0.9962, F1=0.7679, support=264
- Standing: P=0.9216, R=0.5361, F1=0.6779, support=263
