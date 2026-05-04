# ON_PTQ_DEEPCONV_LSTM_CONV2D_E05_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.5341
- Macro-F1: 0.5352

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/on/deepconv_lstm_conv2d/e05/confusion_on_ptq_deepconv_lstm_conv2d_e05_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.3811, R=0.7955, F1=0.5153, support=264
- Jogging: P=0.9745, R=0.5817, F1=0.7286, support=263
- Upstairs: P=0.2521, R=0.2311, F1=0.2411, support=264
- Downstairs: P=0.1148, R=0.0909, F1=0.1015, support=264
- Sitting: P=0.9199, R=1.0000, F1=0.9583, support=264
- Standing: P=0.9779, R=0.5057, F1=0.6667, support=263
