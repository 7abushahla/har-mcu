# ON_PTQ_DEEPCONV_LSTM_CONV2D_E04_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.5303
- Macro-F1: 0.4631

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/deepconv_lstm_conv2d/e04/confusion_on_ptq_deepconv_lstm_conv2d_e04_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.3000, R=0.0341, F1=0.0612, support=264
- Jogging: P=0.8281, R=0.6958, F1=0.7562, support=263
- Upstairs: P=0.3169, R=0.9015, F1=0.4690, support=264
- Downstairs: P=0.3333, R=0.0189, F1=0.0358, support=264
- Sitting: P=0.6368, R=0.9962, F1=0.7770, support=264
- Standing: P=0.9276, R=0.5361, F1=0.6795, support=263
