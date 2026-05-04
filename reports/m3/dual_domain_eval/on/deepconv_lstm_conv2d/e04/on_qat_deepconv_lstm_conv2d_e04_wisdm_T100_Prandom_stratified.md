# ON_QAT_DEEPCONV_LSTM_CONV2D_E04_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/accel_rotation/deepconv_lstm_conv2d/e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.4002
- Macro-F1: 0.2842

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/deepconv_lstm_conv2d/e04/confusion_on_qat_deepconv_lstm_conv2d_e04_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.6871, R=0.3177, F1=0.4345, support=2723
- Jogging: P=0.8997, R=0.5017, F1=0.6441, support=2109
- Upstairs: P=0.1730, R=0.5589, F1=0.2642, support=730
- Downstairs: P=0.1933, R=0.6678, F1=0.2998, support=587
- Sitting: P=1.0000, R=0.0289, F1=0.0561, support=381
- Standing: P=1.0000, R=0.0033, F1=0.0066, support=304
