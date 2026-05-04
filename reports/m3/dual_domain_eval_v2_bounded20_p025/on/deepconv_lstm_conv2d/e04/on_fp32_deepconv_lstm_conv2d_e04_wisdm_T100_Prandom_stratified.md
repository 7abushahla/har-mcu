# ON_FP32_DEEPCONV_LSTM_CONV2D_E04_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.9697
- Macro-F1: 0.9419

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/on/deepconv_lstm_conv2d/e04/confusion_on_fp32_deepconv_lstm_conv2d_e04_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9865, R=0.9938, F1=0.9901, support=2723
- Jogging: P=0.9952, R=0.9919, F1=0.9936, support=2109
- Upstairs: P=0.8397, R=0.9616, F1=0.8966, support=730
- Downstairs: P=0.9612, R=0.8859, F1=0.9220, support=587
- Sitting: P=0.9921, R=0.9895, F1=0.9908, support=381
- Standing: P=0.9914, R=0.7566, F1=0.8582, support=304
