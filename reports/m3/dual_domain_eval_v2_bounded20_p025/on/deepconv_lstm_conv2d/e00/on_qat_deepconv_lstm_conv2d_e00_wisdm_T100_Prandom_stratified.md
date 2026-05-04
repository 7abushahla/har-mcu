# ON_QAT_DEEPCONV_LSTM_CONV2D_E00_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e00/deepconv_lstm_conv2d_T100_Prandom_stratified_E00_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.9473
- Macro-F1: 0.9040

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/on/deepconv_lstm_conv2d/e00/confusion_on_qat_deepconv_lstm_conv2d_e00_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9885, R=0.9750, F1=0.9817, support=2723
- Jogging: P=0.9976, R=0.9701, F1=0.9837, support=2109
- Upstairs: P=0.7240, R=0.9740, F1=0.8306, support=730
- Downstairs: P=0.9257, R=0.8484, F1=0.8853, support=587
- Sitting: P=0.9790, R=0.9790, F1=0.9790, support=381
- Standing: P=0.9745, R=0.6283, F1=0.7640, support=304
