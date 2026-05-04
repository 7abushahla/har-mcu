# OFF_FP32_DEEPCONV_LSTM_CONV2D_E08_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E08_T50_window/no_accel_rotation_v2/deepconv_lstm_conv2d/e08/deepconv_lstm_conv2d_T50_Prandom_stratified_E08_deepconv_lstm_r0_fp32.tflite`
- Model size: 396.43 KB
- Accuracy: 0.9708
- Macro-F1: 0.9565

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025_t50/off/deepconv_lstm_conv2d/e08/confusion_off_fp32_deepconv_lstm_conv2d_e08_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9868, R=0.9838, F1=0.9853, support=5482
- Jogging: P=0.9908, R=0.9911, F1=0.9909, support=4250
- Upstairs: P=0.8844, R=0.9338, F1=0.9085, support=1541
- Downstairs: P=0.9352, R=0.9015, F1=0.9181, support=1249
- Sitting: P=0.9711, R=0.9949, F1=0.9828, support=777
- Standing: P=0.9897, R=0.9199, F1=0.9535, support=624
