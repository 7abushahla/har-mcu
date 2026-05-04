# OFF_QAT_DEEPCONV_LSTM_CONV2D_E07_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E07_skip_inference_norm_diag/no_accel_rotation/deepconv_lstm_conv2d/e07/deepconv_lstm_conv2d_T100_Prandom_stratified_E07_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.9502
- Macro-F1: 0.9231

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/deepconv_lstm_conv2d/e07/confusion_off_qat_deepconv_lstm_conv2d_e07_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9820, R=0.9824, F1=0.9822, support=2723
- Jogging: P=0.9995, R=0.9587, F1=0.9787, support=2109
- Upstairs: P=0.7765, R=0.9425, F1=0.8515, support=730
- Downstairs: P=0.8876, R=0.7802, F1=0.8305, support=587
- Sitting: P=0.9761, R=0.9659, F1=0.9710, support=381
- Standing: P=0.9188, R=0.9309, F1=0.9248, support=304
