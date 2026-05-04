# OFF_PTQ_DEEPCONV_LSTM_CONV2D_E04_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/no_accel_rotation/deepconv_lstm_conv2d/e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.9759
- Macro-F1: 0.9575

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/deepconv_lstm_conv2d/e04/confusion_off_ptq_deepconv_lstm_conv2d_e04_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9897, R=0.9905, F1=0.9901, support=2723
- Jogging: P=0.9943, R=0.9943, F1=0.9943, support=2109
- Upstairs: P=0.8678, R=0.9712, F1=0.9166, support=730
- Downstairs: P=0.9780, R=0.9080, F1=0.9417, support=587
- Sitting: P=0.9921, R=0.9869, F1=0.9895, support=381
- Standing: P=0.9923, R=0.8454, F1=0.9130, support=304
