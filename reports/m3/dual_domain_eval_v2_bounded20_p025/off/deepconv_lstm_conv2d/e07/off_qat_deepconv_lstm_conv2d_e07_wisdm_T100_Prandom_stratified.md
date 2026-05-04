# OFF_QAT_DEEPCONV_LSTM_CONV2D_E07_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E07_skip_inference_norm_diag/no_accel_rotation_v2/deepconv_lstm_conv2d/e07/deepconv_lstm_conv2d_T100_Prandom_stratified_E07_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.8152
- Macro-F1: 0.7653

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/off/deepconv_lstm_conv2d/e07/confusion_off_qat_deepconv_lstm_conv2d_e07_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9451, R=0.8656, F1=0.9036, support=2723
- Jogging: P=0.9801, R=0.7937, F1=0.8771, support=2109
- Upstairs: P=0.5061, R=0.7370, F1=0.6001, support=730
- Downstairs: P=0.5041, R=0.6354, F1=0.5622, support=587
- Sitting: P=0.8172, R=0.9738, F1=0.8886, support=381
- Standing: P=0.6880, R=0.8487, F1=0.7599, support=304
