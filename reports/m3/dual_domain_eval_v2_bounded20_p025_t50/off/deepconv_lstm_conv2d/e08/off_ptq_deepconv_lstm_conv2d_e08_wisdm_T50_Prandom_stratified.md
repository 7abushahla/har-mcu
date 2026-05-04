# OFF_PTQ_DEEPCONV_LSTM_CONV2D_E08_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E08_T50_window/no_accel_rotation_v2/deepconv_lstm_conv2d/e08/deepconv_lstm_conv2d_T50_Prandom_stratified_E08_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 107.62 KB
- Accuracy: 0.9708
- Macro-F1: 0.9559

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025_t50/off/deepconv_lstm_conv2d/e08/confusion_off_ptq_deepconv_lstm_conv2d_e08_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9854, R=0.9852, F1=0.9853, support=5482
- Jogging: P=0.9915, R=0.9920, F1=0.9918, support=4250
- Upstairs: P=0.8834, R=0.9338, F1=0.9079, support=1541
- Downstairs: P=0.9403, R=0.8959, F1=0.9176, support=1249
- Sitting: P=0.9722, R=0.9897, F1=0.9809, support=777
- Standing: P=0.9879, R=0.9183, F1=0.9518, support=624
