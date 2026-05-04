# ON_FP32_DEEPCONV_LSTM_CONV2D_E08_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E08_T50_window/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e08/deepconv_lstm_conv2d_T50_Prandom_stratified_E08_deepconv_lstm_r0_fp32.tflite`
- Model size: 396.43 KB
- Accuracy: 0.9657
- Macro-F1: 0.9451

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/deepconv_lstm_conv2d/e08/confusion_on_fp32_deepconv_lstm_conv2d_e08_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9797, R=0.9880, F1=0.9838, support=5482
- Jogging: P=0.9943, R=0.9824, F1=0.9883, support=4250
- Upstairs: P=0.8768, R=0.9241, F1=0.8998, support=1541
- Downstairs: P=0.9144, R=0.9063, F1=0.9103, support=1249
- Sitting: P=0.9661, R=0.9897, F1=0.9777, support=777
- Standing: P=0.9833, R=0.8478, F1=0.9105, support=624
