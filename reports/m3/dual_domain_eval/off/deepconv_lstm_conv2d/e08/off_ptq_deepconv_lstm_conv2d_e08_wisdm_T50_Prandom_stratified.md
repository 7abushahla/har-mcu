# OFF_PTQ_DEEPCONV_LSTM_CONV2D_E08_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E08_T50_window/no_accel_rotation/deepconv_lstm_conv2d/e08/deepconv_lstm_conv2d_T50_Prandom_stratified_E08_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 107.62 KB
- Accuracy: 0.9700
- Macro-F1: 0.9552

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/deepconv_lstm_conv2d/e08/confusion_off_ptq_deepconv_lstm_conv2d_e08_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9849, R=0.9847, F1=0.9848, support=5482
- Jogging: P=0.9906, R=0.9922, F1=0.9914, support=4250
- Upstairs: P=0.8766, R=0.9312, F1=0.9031, support=1541
- Downstairs: P=0.9423, R=0.8887, F1=0.9147, support=1249
- Sitting: P=0.9784, R=0.9910, F1=0.9847, support=777
- Standing: P=0.9863, R=0.9215, F1=0.9528, support=624
