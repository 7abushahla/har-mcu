# ON_PTQ_DEEPCONV_LSTM_CONV2D_E05_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E05_legacy_arduino_to_mps2/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e05/deepconv_lstm_conv2d_T100_Prandom_stratified_E05_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.9823
- Macro-F1: 0.9728

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/deepconv_lstm_conv2d/e05/confusion_on_ptq_deepconv_lstm_conv2d_e05_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9949, R=0.9938, F1=0.9943, support=2723
- Jogging: P=0.9901, R=0.9957, F1=0.9929, support=2109
- Upstairs: P=0.9146, R=0.9685, F1=0.9408, support=730
- Downstairs: P=0.9758, R=0.8927, F1=0.9324, support=587
- Sitting: P=0.9921, R=0.9869, F1=0.9895, support=381
- Standing: P=0.9868, R=0.9868, F1=0.9868, support=304
