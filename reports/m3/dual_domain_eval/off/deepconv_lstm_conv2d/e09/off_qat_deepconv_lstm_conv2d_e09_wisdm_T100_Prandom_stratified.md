# OFF_QAT_DEEPCONV_LSTM_CONV2D_E09_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/no_accel_rotation/deepconv_lstm_conv2d/e09/deepconv_lstm_conv2d_T100_Prandom_stratified_E09_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.2837
- Macro-F1: 0.0883

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/deepconv_lstm_conv2d/e09/confusion_off_qat_deepconv_lstm_conv2d_e09_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.0996, R=0.0088, F1=0.0162, support=2723
- Jogging: P=0.2992, R=0.8995, F1=0.4490, support=2109
- Upstairs: P=0.0375, R=0.0123, F1=0.0186, support=730
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=587
- Sitting: P=0.7500, R=0.0236, F1=0.0458, support=381
- Standing: P=0.0000, R=0.0000, F1=0.0000, support=304
