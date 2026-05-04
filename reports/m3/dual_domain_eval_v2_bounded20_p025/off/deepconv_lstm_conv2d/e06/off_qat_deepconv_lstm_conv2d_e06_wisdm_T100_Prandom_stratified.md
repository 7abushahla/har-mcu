# OFF_QAT_DEEPCONV_LSTM_CONV2D_E06_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E06_no_norm_matched/no_accel_rotation_v2/deepconv_lstm_conv2d/e06/deepconv_lstm_conv2d_T100_Prandom_stratified_E06_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.9816
- Macro-F1: 0.9664

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/off/deepconv_lstm_conv2d/e06/confusion_off_qat_deepconv_lstm_conv2d_e06_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9941, R=0.9945, F1=0.9943, support=2723
- Jogging: P=0.9986, R=0.9900, F1=0.9943, support=2109
- Upstairs: P=0.9142, R=0.9630, F1=0.9380, support=730
- Downstairs: P=0.9508, R=0.9557, F1=0.9533, support=587
- Sitting: P=0.9844, R=0.9948, F1=0.9896, support=381
- Standing: P=0.9782, R=0.8849, F1=0.9292, support=304
