# OFF_QAT_DEEPCONV_LSTM_CONV2D_E06_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E06_no_norm_matched/no_accel_rotation/deepconv_lstm_conv2d/e06/deepconv_lstm_conv2d_T100_Prandom_stratified_E06_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.9824
- Macro-F1: 0.9692

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/deepconv_lstm_conv2d/e06/confusion_off_qat_deepconv_lstm_conv2d_e06_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9949, R=0.9938, F1=0.9943, support=2723
- Jogging: P=0.9986, R=0.9919, F1=0.9952, support=2109
- Upstairs: P=0.9143, R=0.9644, F1=0.9387, support=730
- Downstairs: P=0.9521, R=0.9489, F1=0.9505, support=587
- Sitting: P=0.9844, R=0.9948, F1=0.9896, support=381
- Standing: P=0.9892, R=0.9079, F1=0.9468, support=304
