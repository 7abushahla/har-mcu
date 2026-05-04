# ON_QAT_DEEPCONV_LSTM_CONV2D_E12_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e12/deepconv_lstm_conv2d_T50_Prandom_stratified_E12_deepconv_lstm_r0_qat.tflite`
- Model size: 108.05 KB
- Accuracy: 0.3341
- Macro-F1: 0.1929

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/on/deepconv_lstm_conv2d/e12/confusion_on_qat_deepconv_lstm_conv2d_e12_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.0909, R=0.0002, F1=0.0004, support=5482
- Jogging: P=0.3270, R=0.9847, F1=0.4909, support=4250
- Upstairs: P=0.1893, R=0.0805, F1=0.1129, support=1541
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=1249
- Sitting: P=0.7478, R=0.4389, F1=0.5531, support=777
- Standing: P=0.0000, R=0.0000, F1=0.0000, support=624
