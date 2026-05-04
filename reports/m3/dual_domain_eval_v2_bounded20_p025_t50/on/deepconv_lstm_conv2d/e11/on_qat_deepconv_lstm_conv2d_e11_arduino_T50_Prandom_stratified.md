# ON_QAT_DEEPCONV_LSTM_CONV2D_E11_ARDUINO TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E11_wisdm_pretrain_arduino_finetune_T50/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e11/deepconv_lstm_conv2d_T50_Prandom_stratified_E11_deepconv_lstm_r0_qat.tflite`
- Model size: 108.05 KB
- Accuracy: 0.9429
- Macro-F1: 0.9433

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025_t50/on/deepconv_lstm_conv2d/e11/confusion_on_qat_deepconv_lstm_conv2d_e11_arduino_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9590, R=0.9735, F1=0.9662, support=529
- Jogging: P=0.9903, R=0.9659, F1=0.9779, support=528
- Upstairs: P=0.8348, R=0.8790, F1=0.8564, support=529
- Downstairs: P=0.8938, R=0.8769, F1=0.8853, support=528
- Sitting: P=0.9981, R=0.9981, F1=0.9981, support=528
- Standing: P=0.9883, R=0.9640, F1=0.9760, support=528
