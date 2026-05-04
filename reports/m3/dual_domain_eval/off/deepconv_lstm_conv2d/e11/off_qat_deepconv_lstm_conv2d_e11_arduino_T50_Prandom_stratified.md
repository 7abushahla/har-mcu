# OFF_QAT_DEEPCONV_LSTM_CONV2D_E11_ARDUINO TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E11_wisdm_pretrain_arduino_finetune_T50/no_accel_rotation/deepconv_lstm_conv2d/e11/deepconv_lstm_conv2d_T50_Prandom_stratified_E11_deepconv_lstm_r0_qat.tflite`
- Model size: 108.05 KB
- Accuracy: 0.9662
- Macro-F1: 0.9662

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/deepconv_lstm_conv2d/e11/confusion_off_qat_deepconv_lstm_conv2d_e11_arduino_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9721, R=0.9868, F1=0.9794, support=529
- Jogging: P=0.9924, R=0.9830, F1=0.9876, support=528
- Upstairs: P=0.9079, R=0.9130, F1=0.9105, support=529
- Downstairs: P=0.9381, R=0.9186, F1=0.9282, support=528
- Sitting: P=0.9925, R=1.0000, F1=0.9962, support=528
- Standing: P=0.9943, R=0.9962, F1=0.9953, support=528
