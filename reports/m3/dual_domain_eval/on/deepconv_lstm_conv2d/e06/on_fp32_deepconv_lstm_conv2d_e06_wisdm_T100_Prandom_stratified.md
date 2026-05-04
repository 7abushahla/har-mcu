# ON_FP32_DEEPCONV_LSTM_CONV2D_E06_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E06_no_norm_matched/accel_rotation/deepconv_lstm_conv2d/e06/deepconv_lstm_conv2d_T100_Prandom_stratified_E06_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.9677
- Macro-F1: 0.9505

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/deepconv_lstm_conv2d/e06/confusion_on_fp32_deepconv_lstm_conv2d_e06_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9916, R=0.9927, F1=0.9921, support=2723
- Jogging: P=0.9965, R=0.9550, F1=0.9753, support=2109
- Upstairs: P=0.8587, R=0.9740, F1=0.9127, support=730
- Downstairs: P=0.9105, R=0.9182, F1=0.9143, support=587
- Sitting: P=0.9972, R=0.9396, F1=0.9676, support=381
- Standing: P=0.9351, R=0.9474, F1=0.9412, support=304
