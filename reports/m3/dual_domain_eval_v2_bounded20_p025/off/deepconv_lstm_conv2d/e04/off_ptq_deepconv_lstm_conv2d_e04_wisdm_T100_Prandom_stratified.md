# OFF_PTQ_DEEPCONV_LSTM_CONV2D_E04_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/no_accel_rotation_v2/deepconv_lstm_conv2d/e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.9843
- Macro-F1: 0.9744

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/off/deepconv_lstm_conv2d/e04/confusion_off_ptq_deepconv_lstm_conv2d_e04_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9945, R=0.9945, F1=0.9945, support=2723
- Jogging: P=0.9952, R=0.9929, F1=0.9941, support=2109
- Upstairs: P=0.9322, R=0.9603, F1=0.9460, support=730
- Downstairs: P=0.9574, R=0.9574, F1=0.9574, support=587
- Sitting: P=0.9895, R=0.9869, F1=0.9882, support=381
- Standing: P=0.9931, R=0.9408, F1=0.9662, support=304
