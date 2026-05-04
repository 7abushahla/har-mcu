# OFF_PTQ_DEEPCONV_LSTM_CONV2D_E10_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E10_arduino_from_scratch/no_accel_rotation/deepconv_lstm_conv2d/e10/deepconv_lstm_conv2d_T100_Prandom_stratified_E10_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.9399
- Macro-F1: 0.9417

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/deepconv_lstm_conv2d/e10/confusion_off_ptq_deepconv_lstm_conv2d_e10_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9913, R=0.8636, F1=0.9231, support=264
- Jogging: P=0.9922, R=0.9696, F1=0.9808, support=263
- Upstairs: P=0.7486, R=0.9811, F1=0.8492, support=264
- Downstairs: P=0.9864, R=0.8258, F1=0.8990, support=264
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=264
- Standing: P=0.9962, R=1.0000, F1=0.9981, support=263
