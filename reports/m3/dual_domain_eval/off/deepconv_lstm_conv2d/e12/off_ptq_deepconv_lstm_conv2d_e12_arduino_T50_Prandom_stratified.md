# OFF_PTQ_DEEPCONV_LSTM_CONV2D_E12_ARDUINO TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/no_accel_rotation/deepconv_lstm_conv2d/e12/deepconv_lstm_conv2d_T50_Prandom_stratified_E12_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 107.62 KB
- Accuracy: 0.8946
- Macro-F1: 0.8982

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/deepconv_lstm_conv2d/e12/confusion_off_ptq_deepconv_lstm_conv2d_e12_arduino_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9613, R=0.8450, F1=0.8994, support=529
- Jogging: P=0.9921, R=0.9470, F1=0.9690, support=528
- Upstairs: P=0.6689, R=0.9471, F1=0.7840, support=529
- Downstairs: P=0.8852, R=0.8617, F1=0.8733, support=528
- Sitting: P=0.9944, R=1.0000, F1=0.9972, support=528
- Standing: P=0.9951, R=0.7670, F1=0.8663, support=528
