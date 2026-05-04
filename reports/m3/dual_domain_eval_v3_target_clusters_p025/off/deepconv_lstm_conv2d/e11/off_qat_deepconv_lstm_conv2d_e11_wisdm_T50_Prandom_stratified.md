# OFF_QAT_DEEPCONV_LSTM_CONV2D_E11_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E11_wisdm_pretrain_arduino_finetune_T50/no_accel_rotation_v2/deepconv_lstm_conv2d/e11/deepconv_lstm_conv2d_T50_Prandom_stratified_E11_deepconv_lstm_r0_qat.tflite`
- Model size: 108.05 KB
- Accuracy: 0.3119
- Macro-F1: 0.1118

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/off/deepconv_lstm_conv2d/e11/confusion_off_qat_deepconv_lstm_conv2d_e11_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.0784, R=0.0007, F1=0.0014, support=5482
- Jogging: P=0.3153, R=1.0000, F1=0.4794, support=4250
- Upstairs: P=0.0405, R=0.0078, F1=0.0131, support=1541
- Downstairs: P=0.0000, R=0.0000, F1=0.0000, support=1249
- Sitting: P=0.8105, R=0.0991, F1=0.1766, support=777
- Standing: P=0.0000, R=0.0000, F1=0.0000, support=624
