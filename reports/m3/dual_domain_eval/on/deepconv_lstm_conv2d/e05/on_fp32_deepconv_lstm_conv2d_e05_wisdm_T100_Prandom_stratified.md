# ON_FP32_DEEPCONV_LSTM_CONV2D_E05_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/accel_rotation/deepconv_lstm_conv2d/e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.9546
- Macro-F1: 0.9115

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/deepconv_lstm_conv2d/e05/confusion_on_fp32_deepconv_lstm_conv2d_e05_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9916, R=0.9912, F1=0.9914, support=2723
- Jogging: P=0.9942, R=0.9763, F1=0.9852, support=2109
- Upstairs: P=0.7587, R=0.9603, F1=0.8476, support=730
- Downstairs: P=0.9268, R=0.9063, F1=0.9165, support=587
- Sitting: P=0.9904, R=0.8136, F1=0.8934, support=381
- Standing: P=0.9696, R=0.7336, F1=0.8352, support=304
