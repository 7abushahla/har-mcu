# OFF_FP32_DEEPCONV_LSTM_CONV2D_E11_ARDUINO TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E11_wisdm_pretrain_arduino_finetune_T50/no_accel_rotation/deepconv_lstm_conv2d/e11/deepconv_lstm_conv2d_T50_Prandom_stratified_E11_deepconv_lstm_r0_fp32.tflite`
- Model size: 396.43 KB
- Accuracy: 0.9735
- Macro-F1: 0.9734

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/deepconv_lstm_conv2d/e11/confusion_off_fp32_deepconv_lstm_conv2d_e11_arduino_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9812, R=0.9887, F1=0.9849, support=529
- Jogging: P=0.9943, R=0.9886, F1=0.9915, support=528
- Upstairs: P=0.9436, R=0.9168, F1=0.9300, support=529
- Downstairs: P=0.9330, R=0.9489, F1=0.9408, support=528
- Sitting: P=0.9925, R=1.0000, F1=0.9962, support=528
- Standing: P=0.9962, R=0.9981, F1=0.9972, support=528
