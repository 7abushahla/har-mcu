# OFF_QAT_DEEPCONV_LSTM_CONV2D_E08_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E08_T50_window/no_accel_rotation_v2/deepconv_lstm_conv2d/e08/deepconv_lstm_conv2d_T50_Prandom_stratified_E08_deepconv_lstm_r0_qat.tflite`
- Model size: 108.05 KB
- Accuracy: 0.9693
- Macro-F1: 0.9532

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/off/deepconv_lstm_conv2d/e08/confusion_off_qat_deepconv_lstm_conv2d_e08_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9845, R=0.9860, F1=0.9852, support=5482
- Jogging: P=0.9957, R=0.9833, F1=0.9895, support=4250
- Upstairs: P=0.8751, R=0.9319, F1=0.9026, support=1541
- Downstairs: P=0.9289, R=0.9199, F1=0.9244, support=1249
- Sitting: P=0.9710, R=0.9910, F1=0.9809, support=777
- Standing: P=0.9858, R=0.8926, F1=0.9369, support=624
