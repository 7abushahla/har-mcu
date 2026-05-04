# OFF_PTQ_DEEPCONV_LSTM_CONV2D_E05_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/no_accel_rotation_v2/deepconv_lstm_conv2d/e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.9801
- Macro-F1: 0.9719

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/off/deepconv_lstm_conv2d/e05/confusion_off_ptq_deepconv_lstm_conv2d_e05_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9937, R=0.9849, F1=0.9893, support=2723
- Jogging: P=0.9948, R=0.9905, F1=0.9926, support=2109
- Upstairs: P=0.9026, R=0.9644, F1=0.9325, support=730
- Downstairs: P=0.9647, R=0.9319, F1=0.9480, support=587
- Sitting: P=0.9843, R=0.9895, F1=0.9869, support=381
- Standing: P=0.9803, R=0.9836, F1=0.9819, support=304
