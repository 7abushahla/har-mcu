# ON_PTQ_DEEPCONV_LSTM_CONV2D_E03_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E03_arduino_downsample_20hz_T100/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e03/deepconv_lstm_conv2d_T100_Prandom_stratified_E03_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.9687
- Macro-F1: 0.9360

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/on/deepconv_lstm_conv2d/e03/confusion_on_ptq_deepconv_lstm_conv2d_e03_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9851, R=0.9963, F1=0.9907, support=2723
- Jogging: P=0.9948, R=0.9924, F1=0.9936, support=2109
- Upstairs: P=0.8372, R=0.9507, F1=0.8903, support=730
- Downstairs: P=0.9587, R=0.9097, F1=0.9336, support=587
- Sitting: P=0.9947, R=0.9790, F1=0.9868, support=381
- Standing: P=0.9907, R=0.7007, F1=0.8208, support=304
