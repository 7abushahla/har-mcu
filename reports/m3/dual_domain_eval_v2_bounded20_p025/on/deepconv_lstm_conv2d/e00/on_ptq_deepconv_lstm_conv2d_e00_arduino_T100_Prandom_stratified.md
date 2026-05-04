# ON_PTQ_DEEPCONV_LSTM_CONV2D_E00_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e00/deepconv_lstm_conv2d_T100_Prandom_stratified_E00_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.1669
- Macro-F1: 0.0477

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/on/deepconv_lstm_conv2d/e00/confusion_on_ptq_deepconv_lstm_conv2d_e00_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.0000, R=0.0000, F1=0.0000, support=264
- Jogging: P=0.0000, R=0.0000, F1=0.0000, support=263
- Upstairs: P=0.0000, R=0.0000, F1=0.0000, support=264
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=264
- Sitting: P=0.1669, R=1.0000, F1=0.2860, support=264
- Standing: P=0.0000, R=0.0000, F1=0.0000, support=263
