# ON_QAT_DEEPCONV_LSTM_CONV2D_E05_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.8992
- Macro-F1: 0.8413

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/on/deepconv_lstm_conv2d/e05/confusion_on_qat_deepconv_lstm_conv2d_e05_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9842, R=0.9394, F1=0.9613, support=2723
- Jogging: P=0.9984, R=0.9118, F1=0.9532, support=2109
- Upstairs: P=0.5869, R=0.9479, F1=0.7250, support=730
- Downstairs: P=0.7675, R=0.7479, F1=0.7575, support=587
- Sitting: P=0.9609, R=0.9685, F1=0.9647, support=381
- Standing: P=0.9425, R=0.5395, F1=0.6862, support=304
