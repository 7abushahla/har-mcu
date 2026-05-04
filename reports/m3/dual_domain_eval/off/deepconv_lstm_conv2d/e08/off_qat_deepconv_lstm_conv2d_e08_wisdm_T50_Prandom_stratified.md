# OFF_QAT_DEEPCONV_LSTM_CONV2D_E08_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E08_T50_window/no_accel_rotation/deepconv_lstm_conv2d/e08/deepconv_lstm_conv2d_T50_Prandom_stratified_E08_deepconv_lstm_r0_qat.tflite`
- Model size: 108.05 KB
- Accuracy: 0.9689
- Macro-F1: 0.9539

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/deepconv_lstm_conv2d/e08/confusion_off_qat_deepconv_lstm_conv2d_e08_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9840, R=0.9852, F1=0.9846, support=5482
- Jogging: P=0.9952, R=0.9816, F1=0.9884, support=4250
- Upstairs: P=0.8757, R=0.9280, F1=0.9011, support=1541
- Downstairs: P=0.9240, R=0.9247, F1=0.9244, support=1249
- Sitting: P=0.9735, R=0.9910, F1=0.9821, support=777
- Standing: P=0.9894, R=0.9006, F1=0.9430, support=624
