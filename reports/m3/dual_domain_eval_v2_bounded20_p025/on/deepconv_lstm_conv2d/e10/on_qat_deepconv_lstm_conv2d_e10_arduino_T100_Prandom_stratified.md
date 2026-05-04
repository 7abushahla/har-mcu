# ON_QAT_DEEPCONV_LSTM_CONV2D_E10_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E10_arduino_from_scratch/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e10/deepconv_lstm_conv2d_T100_Prandom_stratified_E10_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.4456
- Macro-F1: 0.4557

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/on/deepconv_lstm_conv2d/e10/confusion_on_qat_deepconv_lstm_conv2d_e10_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.4779, R=0.7765, F1=0.5916, support=264
- Jogging: P=0.9663, R=0.3270, F1=0.4886, support=263
- Upstairs: P=0.1802, R=0.3030, F1=0.2260, support=264
- Downstairs: P=0.3383, R=0.5114, F1=0.4072, support=264
- Sitting: P=0.9828, R=0.2159, F1=0.3540, support=264
- Standing: P=0.8712, R=0.5399, F1=0.6667, support=263
