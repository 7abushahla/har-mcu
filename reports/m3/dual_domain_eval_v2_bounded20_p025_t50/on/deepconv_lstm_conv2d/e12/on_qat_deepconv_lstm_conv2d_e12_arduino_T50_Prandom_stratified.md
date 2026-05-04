# ON_QAT_DEEPCONV_LSTM_CONV2D_E12_ARDUINO TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e12/deepconv_lstm_conv2d_T50_Prandom_stratified_E12_deepconv_lstm_r0_qat.tflite`
- Model size: 108.05 KB
- Accuracy: 0.8076
- Macro-F1: 0.8129

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025_t50/on/deepconv_lstm_conv2d/e12/confusion_on_qat_deepconv_lstm_conv2d_e12_arduino_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.8563, R=0.8110, F1=0.8330, support=529
- Jogging: P=0.9721, R=0.8580, F1=0.9115, support=528
- Upstairs: P=0.6673, R=0.6408, F1=0.6538, support=529
- Downstairs: P=0.5720, R=0.8580, F1=0.6864, support=528
- Sitting: P=0.9906, R=1.0000, F1=0.9953, support=528
- Standing: P=0.9676, R=0.6780, F1=0.7973, support=528
