# OFF_FP32_DEEPCONV_LSTM_CONV2D_E11_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E11_wisdm_pretrain_arduino_finetune_T50/no_accel_rotation_v2/deepconv_lstm_conv2d/e11/deepconv_lstm_conv2d_T50_Prandom_stratified_E11_deepconv_lstm_r0_fp32.tflite`
- Model size: 396.43 KB
- Accuracy: 0.3062
- Macro-F1: 0.0888

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025_t50/off/deepconv_lstm_conv2d/e11/confusion_off_fp32_deepconv_lstm_conv2d_e11_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.0259, R=0.0016, F1=0.0031, support=5482
- Jogging: P=0.3182, R=0.9944, F1=0.4821, support=4250
- Upstairs: P=0.0395, R=0.0058, F1=0.0102, support=1541
- Downstairs: P=0.3438, R=0.0088, F1=0.0172, support=1249
- Sitting: P=0.8889, R=0.0103, F1=0.0204, support=777
- Standing: P=0.0000, R=0.0000, F1=0.0000, support=624
