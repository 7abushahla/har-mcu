# ON_QAT_DEEPCONV_LSTM_CONV2D_E05_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/accel_rotation/deepconv_lstm_conv2d/e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.3414
- Macro-F1: 0.2463

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/deepconv_lstm_conv2d/e05/confusion_on_qat_deepconv_lstm_conv2d_e05_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.6938, R=0.2347, F1=0.3507, support=2723
- Jogging: P=0.9460, R=0.3988, F1=0.5610, support=2109
- Upstairs: P=0.1756, R=0.5836, F1=0.2700, support=730
- Downstairs: P=0.1625, R=0.7172, F1=0.2649, support=587
- Sitting: P=0.8571, R=0.0157, F1=0.0309, support=381
- Standing: P=0.0000, R=0.0000, F1=0.0000, support=304
