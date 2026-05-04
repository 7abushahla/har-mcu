# ON_QAT_DEEPCONV_LSTM_CONV2D_E06_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E06_no_norm_matched/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e06/deepconv_lstm_conv2d_T100_Prandom_stratified_E06_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.9641
- Macro-F1: 0.9396

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/on/deepconv_lstm_conv2d/e06/confusion_on_qat_deepconv_lstm_conv2d_e06_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9925, R=0.9717, F1=0.9820, support=2723
- Jogging: P=0.9981, R=0.9891, F1=0.9936, support=2109
- Upstairs: P=0.7948, R=0.9712, F1=0.8742, support=730
- Downstairs: P=0.9434, R=0.9080, F1=0.9253, support=587
- Sitting: P=0.9948, R=0.9948, F1=0.9948, support=381
- Standing: P=0.9833, R=0.7763, F1=0.8676, support=304
