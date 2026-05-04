# ON_QAT_DEEPCONV_LSTM_CONV2D_E11_ARDUINO TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E11_wisdm_pretrain_arduino_finetune_T50/accel_rotation/deepconv_lstm_conv2d/e11/deepconv_lstm_conv2d_T50_Prandom_stratified_E11_deepconv_lstm_r0_qat.tflite`
- Model size: 108.05 KB
- Accuracy: 0.7987
- Macro-F1: 0.8022

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/deepconv_lstm_conv2d/e11/confusion_on_qat_deepconv_lstm_conv2d_e11_arduino_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.7174, R=0.9263, F1=0.8086, support=529
- Jogging: P=0.9775, R=0.9053, F1=0.9400, support=528
- Upstairs: P=0.5801, R=0.5955, F1=0.5877, support=529
- Downstairs: P=0.7043, R=0.7670, F1=0.7344, support=528
- Sitting: P=0.9978, R=0.8523, F1=0.9193, support=528
- Standing: P=0.9184, R=0.7462, F1=0.8234, support=528
