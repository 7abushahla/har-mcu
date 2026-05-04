# OFF_PTQ_DEEPCONV_LSTM_CONV2D_E08_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E08_T50_window/no_accel_rotation_v2/deepconv_lstm_conv2d/e08/deepconv_lstm_conv2d_T50_Prandom_stratified_E08_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 107.62 KB
- Accuracy: 0.9703
- Macro-F1: 0.9544

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/off/deepconv_lstm_conv2d/e08/confusion_off_ptq_deepconv_lstm_conv2d_e08_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9851, R=0.9858, F1=0.9854, support=5482
- Jogging: P=0.9918, R=0.9915, F1=0.9916, support=4250
- Upstairs: P=0.8759, R=0.9345, F1=0.9042, support=1541
- Downstairs: P=0.9444, R=0.8975, F1=0.9204, support=1249
- Sitting: P=0.9759, R=0.9910, F1=0.9834, support=777
- Standing: P=0.9877, R=0.8990, F1=0.9413, support=624
