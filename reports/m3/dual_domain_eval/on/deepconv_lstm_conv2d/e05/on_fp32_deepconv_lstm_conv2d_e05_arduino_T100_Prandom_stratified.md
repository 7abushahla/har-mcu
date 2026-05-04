# ON_FP32_DEEPCONV_LSTM_CONV2D_E05_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/accel_rotation/deepconv_lstm_conv2d/e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.5430
- Macro-F1: 0.5136

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/deepconv_lstm_conv2d/e05/confusion_on_fp32_deepconv_lstm_conv2d_e05_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.2749, R=0.3030, F1=0.2883, support=264
- Jogging: P=0.7314, R=0.9734, F1=0.8352, support=263
- Upstairs: P=0.2756, R=0.3674, F1=0.3149, support=264
- Downstairs: P=0.4545, R=0.0947, F1=0.1567, support=264
- Sitting: P=0.6650, R=0.9924, F1=0.7964, support=264
- Standing: P=0.9929, R=0.5285, F1=0.6898, support=263
