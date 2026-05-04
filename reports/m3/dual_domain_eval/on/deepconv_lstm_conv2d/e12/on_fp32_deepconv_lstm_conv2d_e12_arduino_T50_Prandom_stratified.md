# ON_FP32_DEEPCONV_LSTM_CONV2D_E12_ARDUINO TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/accel_rotation/deepconv_lstm_conv2d/e12/deepconv_lstm_conv2d_T50_Prandom_stratified_E12_deepconv_lstm_r0_fp32.tflite`
- Model size: 396.43 KB
- Accuracy: 0.9120
- Macro-F1: 0.9126

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/deepconv_lstm_conv2d/e12/confusion_on_fp32_deepconv_lstm_conv2d_e12_arduino_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9066, R=0.9357, F1=0.9209, support=529
- Jogging: P=0.9841, R=0.9394, F1=0.9612, support=528
- Upstairs: P=0.7784, R=0.8034, F1=0.7907, support=529
- Downstairs: P=0.8175, R=0.8144, F1=0.8159, support=528
- Sitting: P=0.9962, R=0.9886, F1=0.9924, support=528
- Standing: P=0.9981, R=0.9905, F1=0.9943, support=528
