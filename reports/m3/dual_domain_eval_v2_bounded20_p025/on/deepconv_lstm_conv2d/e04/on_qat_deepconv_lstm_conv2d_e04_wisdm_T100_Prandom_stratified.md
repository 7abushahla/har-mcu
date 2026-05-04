# ON_QAT_DEEPCONV_LSTM_CONV2D_E04_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.8944
- Macro-F1: 0.8369

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/on/deepconv_lstm_conv2d/e04/confusion_on_qat_deepconv_lstm_conv2d_e04_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9770, R=0.9357, F1=0.9559, support=2723
- Jogging: P=0.9974, R=0.9033, F1=0.9480, support=2109
- Upstairs: P=0.6054, R=0.9247, F1=0.7317, support=730
- Downstairs: P=0.7173, R=0.7564, F1=0.7363, support=587
- Sitting: P=0.9270, R=0.9659, F1=0.9460, support=381
- Standing: P=0.9297, R=0.5658, F1=0.7035, support=304
