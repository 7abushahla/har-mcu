# OFF_PTQ_DEEPCONV_LSTM_CONV2D_E11_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E11_wisdm_pretrain_arduino_finetune_T50/no_accel_rotation_v2/deepconv_lstm_conv2d/e11/deepconv_lstm_conv2d_T50_Prandom_stratified_E11_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 107.62 KB
- Accuracy: 0.3109
- Macro-F1: 0.1088

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025_t50/off/deepconv_lstm_conv2d/e11/confusion_off_ptq_deepconv_lstm_conv2d_e11_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.0000, R=0.0000, F1=0.0000, support=5482
- Jogging: P=0.3151, R=0.9998, F1=0.4791, support=4250
- Upstairs: P=0.0257, R=0.0045, F1=0.0077, support=1541
- Downstairs: P=0.0612, R=0.0024, F1=0.0046, support=1249
- Sitting: P=0.8095, R=0.0875, F1=0.1580, support=777
- Standing: P=0.3333, R=0.0016, F1=0.0032, support=624
