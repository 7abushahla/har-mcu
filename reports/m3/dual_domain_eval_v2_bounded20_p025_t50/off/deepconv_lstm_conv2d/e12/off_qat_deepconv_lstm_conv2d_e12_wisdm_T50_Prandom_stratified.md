# OFF_QAT_DEEPCONV_LSTM_CONV2D_E12_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/no_accel_rotation_v2/deepconv_lstm_conv2d/e12/deepconv_lstm_conv2d_T50_Prandom_stratified_E12_deepconv_lstm_r0_qat.tflite`
- Model size: 108.05 KB
- Accuracy: 0.3187
- Macro-F1: 0.1695

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025_t50/off/deepconv_lstm_conv2d/e12/confusion_off_qat_deepconv_lstm_conv2d_e12_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.2461, R=0.0144, F1=0.0272, support=5482
- Jogging: P=0.3384, R=0.9096, F1=0.4933, support=4250
- Upstairs: P=0.1562, R=0.1343, F1=0.1445, support=1541
- Downstairs: P=0.1429, R=0.0008, F1=0.0016, support=1249
- Sitting: P=0.3361, R=0.3655, F1=0.3502, support=777
- Standing: P=0.0000, R=0.0000, F1=0.0000, support=624
