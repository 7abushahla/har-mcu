# ON_QAT_DEEPCONV_LSTM_CONV2D_E06_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E06_no_norm_matched/accel_rotation/deepconv_lstm_conv2d/e06/deepconv_lstm_conv2d_T100_Prandom_stratified_E06_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.9545
- Macro-F1: 0.9147

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/deepconv_lstm_conv2d/e06/confusion_on_qat_deepconv_lstm_conv2d_e06_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9890, R=0.9897, F1=0.9894, support=2723
- Jogging: P=0.9970, R=0.9554, F1=0.9758, support=2109
- Upstairs: P=0.7939, R=0.9603, F1=0.8692, support=730
- Downstairs: P=0.8728, R=0.9353, F1=0.9030, support=587
- Sitting: P=0.9918, R=0.9501, F1=0.9705, support=381
- Standing: P=0.9526, R=0.6612, F1=0.7806, support=304
