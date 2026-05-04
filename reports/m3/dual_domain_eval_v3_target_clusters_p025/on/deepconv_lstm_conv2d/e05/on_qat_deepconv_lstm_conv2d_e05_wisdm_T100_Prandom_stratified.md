# ON_QAT_DEEPCONV_LSTM_CONV2D_E05_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.8203
- Macro-F1: 0.7947

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/deepconv_lstm_conv2d/e05/confusion_on_qat_deepconv_lstm_conv2d_e05_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.8944, R=0.8153, F1=0.8530, support=2723
- Jogging: P=0.9961, R=0.8478, F1=0.9160, support=2109
- Upstairs: P=0.5050, R=0.7589, F1=0.6065, support=730
- Downstairs: P=0.5805, R=0.8109, F1=0.6766, support=587
- Sitting: P=0.9127, R=0.7953, F1=0.8499, support=381
- Standing: P=0.8604, R=0.8717, F1=0.8660, support=304
