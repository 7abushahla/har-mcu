# ON_QAT_DEEPCONV_LSTM_CONV2D_E10_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E10_arduino_from_scratch/accel_rotation/deepconv_lstm_conv2d/e10/deepconv_lstm_conv2d_T100_Prandom_stratified_E10_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.3142
- Macro-F1: 0.2989

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/deepconv_lstm_conv2d/e10/confusion_on_qat_deepconv_lstm_conv2d_e10_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.7347, R=0.1364, F1=0.2300, support=264
- Jogging: P=1.0000, R=0.5703, F1=0.7264, support=263
- Upstairs: P=0.1851, R=0.8106, F1=0.3014, support=264
- Downstairs: P=0.2800, R=0.1856, F1=0.2232, support=264
- Sitting: P=0.3333, R=0.0076, F1=0.0148, support=264
- Standing: P=1.0000, R=0.1749, F1=0.2977, support=263
