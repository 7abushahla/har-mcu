# ON_PTQ_DEEPCONV_LSTM_CONV2D_E05_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/accel_rotation/deepconv_lstm_conv2d/e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.5461
- Macro-F1: 0.5190

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/deepconv_lstm_conv2d/e05/confusion_on_ptq_deepconv_lstm_conv2d_e05_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.2876, R=0.3258, F1=0.3055, support=264
- Jogging: P=0.7636, R=0.9582, F1=0.8499, support=263
- Upstairs: P=0.2787, R=0.3864, F1=0.3238, support=264
- Downstairs: P=0.4364, R=0.0909, F1=0.1505, support=264
- Sitting: P=0.6667, R=0.9924, F1=0.7976, support=264
- Standing: P=0.9928, R=0.5247, F1=0.6866, support=263
