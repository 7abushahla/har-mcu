# OFF_PTQ_DEEPCONV_LSTM_CONV2D_E05_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/no_accel_rotation_v2/deepconv_lstm_conv2d/e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.5329
- Macro-F1: 0.5475

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/off/deepconv_lstm_conv2d/e05/confusion_off_ptq_deepconv_lstm_conv2d_e05_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.3596, R=0.6061, F1=0.4513, support=264
- Jogging: P=1.0000, R=0.5095, F1=0.6751, support=263
- Upstairs: P=0.3151, R=0.3485, F1=0.3309, support=264
- Downstairs: P=0.2403, R=0.2576, F1=0.2486, support=264
- Sitting: P=0.9429, R=1.0000, F1=0.9706, support=264
- Standing: P=0.8446, R=0.4753, F1=0.6083, support=263
