# OFF_QAT_DEEPCONV_LSTM_CONV2D_E00_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/no_accel_rotation_v2/deepconv_lstm_conv2d/e00/deepconv_lstm_conv2d_T100_Prandom_stratified_E00_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.9388
- Macro-F1: 0.9102

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/off/deepconv_lstm_conv2d/e00/confusion_off_qat_deepconv_lstm_conv2d_e00_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9793, R=0.9747, F1=0.9770, support=2723
- Jogging: P=0.9995, R=0.9403, F1=0.9690, support=2109
- Upstairs: P=0.7497, R=0.9192, F1=0.8258, support=730
- Downstairs: P=0.8387, R=0.7530, F1=0.7935, support=587
- Sitting: P=0.9683, R=0.9633, F1=0.9658, support=381
- Standing: P=0.8820, R=0.9836, F1=0.9300, support=304
