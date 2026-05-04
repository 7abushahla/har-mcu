# OFF_FP32_DEEPCONV_LSTM_CONV2D_E10_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E10_arduino_from_scratch/no_accel_rotation_v2/deepconv_lstm_conv2d/e10/deepconv_lstm_conv2d_T100_Prandom_stratified_E10_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.9406
- Macro-F1: 0.9405

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/off/deepconv_lstm_conv2d/e10/confusion_off_fp32_deepconv_lstm_conv2d_e10_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9721, R=0.9242, F1=0.9476, support=264
- Jogging: P=0.9885, R=0.9848, F1=0.9867, support=263
- Upstairs: P=0.7853, R=0.9697, F1=0.8678, support=264
- Downstairs: P=0.9902, R=0.7652, F1=0.8632, support=264
- Sitting: P=0.9670, R=1.0000, F1=0.9832, support=264
- Standing: P=0.9887, R=1.0000, F1=0.9943, support=263
