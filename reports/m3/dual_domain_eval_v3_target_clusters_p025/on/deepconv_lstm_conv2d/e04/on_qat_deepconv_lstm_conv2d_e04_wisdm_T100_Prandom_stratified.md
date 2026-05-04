# ON_QAT_DEEPCONV_LSTM_CONV2D_E04_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.8405
- Macro-F1: 0.8061

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/deepconv_lstm_conv2d/e04/confusion_on_qat_deepconv_lstm_conv2d_e04_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9014, R=0.8524, F1=0.8762, support=2723
- Jogging: P=0.9973, R=0.8663, F1=0.9272, support=2109
- Upstairs: P=0.5551, R=0.7589, F1=0.6412, support=730
- Downstairs: P=0.6097, R=0.8330, F1=0.7041, support=587
- Sitting: P=0.9021, R=0.7743, F1=0.8333, support=381
- Standing: P=0.8600, R=0.8487, F1=0.8543, support=304
