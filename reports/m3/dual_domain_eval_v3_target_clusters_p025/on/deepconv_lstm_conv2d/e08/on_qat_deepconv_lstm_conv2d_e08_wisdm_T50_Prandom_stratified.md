# ON_QAT_DEEPCONV_LSTM_CONV2D_E08_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E08_T50_window/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e08/deepconv_lstm_conv2d_T50_Prandom_stratified_E08_deepconv_lstm_r0_qat.tflite`
- Model size: 108.05 KB
- Accuracy: 0.9481
- Macro-F1: 0.9168

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/deepconv_lstm_conv2d/e08/confusion_on_qat_deepconv_lstm_conv2d_e08_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9720, R=0.9830, F1=0.9775, support=5482
- Jogging: P=0.9935, R=0.9642, F1=0.9786, support=4250
- Upstairs: P=0.8027, R=0.9001, F1=0.8486, support=1541
- Downstairs: P=0.8888, R=0.8895, F1=0.8892, support=1249
- Sitting: P=0.9724, R=0.9073, F1=0.9387, support=777
- Standing: P=0.9256, R=0.8173, F1=0.8681, support=624
