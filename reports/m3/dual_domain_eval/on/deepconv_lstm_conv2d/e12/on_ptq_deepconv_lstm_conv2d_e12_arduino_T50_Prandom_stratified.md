# ON_PTQ_DEEPCONV_LSTM_CONV2D_E12_ARDUINO TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/accel_rotation/deepconv_lstm_conv2d/e12/deepconv_lstm_conv2d_T50_Prandom_stratified_E12_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 107.62 KB
- Accuracy: 0.9114
- Macro-F1: 0.9120

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/deepconv_lstm_conv2d/e12/confusion_on_ptq_deepconv_lstm_conv2d_e12_arduino_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9036, R=0.9395, F1=0.9212, support=529
- Jogging: P=0.9841, R=0.9375, F1=0.9602, support=528
- Upstairs: P=0.7736, R=0.8072, F1=0.7900, support=529
- Downstairs: P=0.8231, R=0.8106, F1=0.8168, support=528
- Sitting: P=0.9962, R=0.9867, F1=0.9914, support=528
- Standing: P=0.9981, R=0.9867, F1=0.9924, support=528
