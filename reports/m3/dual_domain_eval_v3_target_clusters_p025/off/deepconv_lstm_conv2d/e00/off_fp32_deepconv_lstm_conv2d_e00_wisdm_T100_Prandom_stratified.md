# OFF_FP32_DEEPCONV_LSTM_CONV2D_E00_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E00_wisdm_m2_anchor/no_accel_rotation_v2/deepconv_lstm_conv2d/e00/deepconv_lstm_conv2d_T100_Prandom_stratified_E00_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.9783
- Macro-F1: 0.9682

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/off/deepconv_lstm_conv2d/e00/confusion_off_fp32_deepconv_lstm_conv2d_e00_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9919, R=0.9875, F1=0.9897, support=2723
- Jogging: P=0.9967, R=0.9877, F1=0.9921, support=2109
- Upstairs: P=0.9001, R=0.9507, F1=0.9247, support=730
- Downstairs: P=0.9466, R=0.9370, F1=0.9418, support=587
- Sitting: P=0.9817, R=0.9869, F1=0.9843, support=381
- Standing: P=0.9866, R=0.9671, F1=0.9767, support=304
