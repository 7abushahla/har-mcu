# ON_FP32_DEEPCONV_LSTM_CONV2D_E04_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/accel_rotation_v3_target_clusters_p025/deepconv_lstm_conv2d/e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.9854
- Macro-F1: 0.9768

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/on/deepconv_lstm_conv2d/e04/confusion_on_fp32_deepconv_lstm_conv2d_e04_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9985, R=0.9938, F1=0.9961, support=2723
- Jogging: P=0.9915, R=0.9957, F1=0.9936, support=2109
- Upstairs: P=0.9282, R=0.9740, F1=0.9505, support=730
- Downstairs: P=0.9783, R=0.9216, F1=0.9491, support=587
- Sitting: P=0.9843, R=0.9843, F1=0.9843, support=381
- Standing: P=0.9837, R=0.9901, F1=0.9869, support=304
