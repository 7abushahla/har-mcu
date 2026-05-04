# OFF_FP32_DEEPCONV_LSTM_CONV2D_E10_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E10_arduino_from_scratch/no_accel_rotation_v2/deepconv_lstm_conv2d/e10/deepconv_lstm_conv2d_T100_Prandom_stratified_E10_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.3493
- Macro-F1: 0.2245

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/off/deepconv_lstm_conv2d/e10/confusion_off_fp32_deepconv_lstm_conv2d_e10_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.3333, R=0.0007, F1=0.0015, support=2723
- Jogging: P=0.3947, R=0.9317, F1=0.5545, support=2109
- Upstairs: P=0.2005, R=0.3082, F1=0.2430, support=730
- Downstairs: P=0.0862, R=0.0647, F1=0.0739, support=587
- Sitting: P=0.5587, R=0.4121, F1=0.4743, support=381
- Standing: P=0.0000, R=0.0000, F1=0.0000, support=304
