# OFF_FP32_DEEPCONV_LSTM_CONV2D_E08_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E08_T50_window/no_accel_rotation/deepconv_lstm_conv2d/e08/deepconv_lstm_conv2d_T50_Prandom_stratified_E08_deepconv_lstm_r0_fp32.tflite`
- Model size: 396.43 KB
- Accuracy: 0.9703
- Macro-F1: 0.9560

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/deepconv_lstm_conv2d/e08/confusion_off_fp32_deepconv_lstm_conv2d_e08_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9863, R=0.9839, F1=0.9851, support=5482
- Jogging: P=0.9906, R=0.9920, F1=0.9913, support=4250
- Upstairs: P=0.8778, R=0.9319, F1=0.9040, support=1541
- Downstairs: P=0.9386, R=0.8927, F1=0.9151, support=1249
- Sitting: P=0.9772, R=0.9949, F1=0.9860, support=777
- Standing: P=0.9880, R=0.9231, F1=0.9544, support=624
