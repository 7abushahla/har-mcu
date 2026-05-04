# OFF_QAT_DEEPCONV_LSTM_CONV2D_E04_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/no_accel_rotation_v2/deepconv_lstm_conv2d/e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.9631
- Macro-F1: 0.9420

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/off/deepconv_lstm_conv2d/e04/confusion_off_qat_deepconv_lstm_conv2d_e04_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9846, R=0.9868, F1=0.9857, support=2723
- Jogging: P=0.9990, R=0.9716, F1=0.9851, support=2109
- Upstairs: P=0.8153, R=0.9616, F1=0.8825, support=730
- Downstairs: P=0.9487, R=0.8501, F1=0.8967, support=587
- Sitting: P=0.9738, R=0.9764, F1=0.9751, support=381
- Standing: P=0.9579, R=0.8980, F1=0.9270, support=304
