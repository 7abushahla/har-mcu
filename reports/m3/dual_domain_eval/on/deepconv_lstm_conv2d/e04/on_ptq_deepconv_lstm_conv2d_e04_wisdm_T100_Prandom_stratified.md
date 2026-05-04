# ON_PTQ_DEEPCONV_LSTM_CONV2D_E04_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/accel_rotation/deepconv_lstm_conv2d/e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.9552
- Macro-F1: 0.9100

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/deepconv_lstm_conv2d/e04/confusion_on_ptq_deepconv_lstm_conv2d_e04_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9908, R=0.9923, F1=0.9916, support=2723
- Jogging: P=0.9942, R=0.9791, F1=0.9866, support=2109
- Upstairs: P=0.7625, R=0.9630, F1=0.8511, support=730
- Downstairs: P=0.9431, R=0.9029, F1=0.9225, support=587
- Sitting: P=0.9903, R=0.8005, F1=0.8853, support=381
- Standing: P=0.9370, R=0.7336, F1=0.8229, support=304
