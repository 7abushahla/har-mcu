# ON_PTQ_DEEPCONV_LSTM_CONV2D_E08_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E08_T50_window/accel_rotation/deepconv_lstm_conv2d/e08/deepconv_lstm_conv2d_T50_Prandom_stratified_E08_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 107.62 KB
- Accuracy: 0.9623
- Macro-F1: 0.9488

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/deepconv_lstm_conv2d/e08/confusion_on_ptq_deepconv_lstm_conv2d_e08_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9809, R=0.9818, F1=0.9813, support=5482
- Jogging: P=0.9890, R=0.9751, F1=0.9820, support=4250
- Upstairs: P=0.8932, R=0.8897, F1=0.8914, support=1541
- Downstairs: P=0.8648, R=0.9063, F1=0.8851, support=1249
- Sitting: P=0.9734, R=0.9871, F1=0.9802, support=777
- Standing: P=0.9805, R=0.9647, F1=0.9725, support=624
