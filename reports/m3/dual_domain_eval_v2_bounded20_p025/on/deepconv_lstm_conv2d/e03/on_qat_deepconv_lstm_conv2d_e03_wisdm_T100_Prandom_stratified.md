# ON_QAT_DEEPCONV_LSTM_CONV2D_E03_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E03_arduino_downsample_20hz_T100/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e03/deepconv_lstm_conv2d_T100_Prandom_stratified_E03_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.9399
- Macro-F1: 0.8907

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/on/deepconv_lstm_conv2d/e03/confusion_on_qat_deepconv_lstm_conv2d_e03_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9851, R=0.9706, F1=0.9778, support=2723
- Jogging: P=0.9980, R=0.9701, F1=0.9839, support=2109
- Upstairs: P=0.6921, R=0.9575, F1=0.8034, support=730
- Downstairs: P=0.9171, R=0.8296, F1=0.8712, support=587
- Sitting: P=0.9919, R=0.9685, F1=0.9801, support=381
- Standing: P=0.9521, R=0.5888, F1=0.7276, support=304
