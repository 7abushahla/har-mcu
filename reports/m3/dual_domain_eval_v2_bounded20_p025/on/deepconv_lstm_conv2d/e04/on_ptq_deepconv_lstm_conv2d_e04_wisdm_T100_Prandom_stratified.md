# ON_PTQ_DEEPCONV_LSTM_CONV2D_E04_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E04_wisdm_to_g_arduino_g/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e04/deepconv_lstm_conv2d_T100_Prandom_stratified_E04_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.9701
- Macro-F1: 0.9430

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/on/deepconv_lstm_conv2d/e04/confusion_on_ptq_deepconv_lstm_conv2d_e04_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9862, R=0.9941, F1=0.9901, support=2723
- Jogging: P=0.9952, R=0.9924, F1=0.9938, support=2109
- Upstairs: P=0.8438, R=0.9616, F1=0.8988, support=730
- Downstairs: P=0.9610, R=0.8825, F1=0.9201, support=587
- Sitting: P=0.9921, R=0.9895, F1=0.9908, support=381
- Standing: P=0.9915, R=0.7664, F1=0.8646, support=304
