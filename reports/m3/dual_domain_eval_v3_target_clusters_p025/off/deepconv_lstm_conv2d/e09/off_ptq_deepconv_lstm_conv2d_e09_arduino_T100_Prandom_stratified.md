# OFF_PTQ_DEEPCONV_LSTM_CONV2D_E09_ARDUINO TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E09_wisdm_pretrain_arduino_finetune/no_accel_rotation_v2/deepconv_lstm_conv2d/e09/deepconv_lstm_conv2d_T100_Prandom_stratified_E09_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.9886
- Macro-F1: 0.9886

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/off/deepconv_lstm_conv2d/e09/confusion_off_ptq_deepconv_lstm_conv2d_e09_arduino_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9924, R=0.9886, F1=0.9905, support=264
- Jogging: P=0.9924, R=0.9886, F1=0.9905, support=263
- Upstairs: P=0.9630, R=0.9848, F1=0.9738, support=264
- Downstairs: P=0.9846, R=0.9697, F1=0.9771, support=264
- Sitting: P=1.0000, R=1.0000, F1=1.0000, support=264
- Standing: P=1.0000, R=1.0000, F1=1.0000, support=263
