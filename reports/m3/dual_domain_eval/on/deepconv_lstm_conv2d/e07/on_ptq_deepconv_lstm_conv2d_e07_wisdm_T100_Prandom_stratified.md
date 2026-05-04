# ON_PTQ_DEEPCONV_LSTM_CONV2D_E07_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E07_skip_inference_norm_diag/accel_rotation/deepconv_lstm_conv2d/e07/deepconv_lstm_conv2d_T100_Prandom_stratified_E07_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.9497
- Macro-F1: 0.8985

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/deepconv_lstm_conv2d/e07/confusion_on_ptq_deepconv_lstm_conv2d_e07_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9912, R=0.9919, F1=0.9916, support=2723
- Jogging: P=0.9942, R=0.9763, F1=0.9852, support=2109
- Upstairs: P=0.7300, R=0.9630, F1=0.8305, support=730
- Downstairs: P=0.9357, R=0.8927, F1=0.9137, support=587
- Sitting: P=0.9898, R=0.7638, F1=0.8622, support=381
- Standing: P=0.9593, R=0.6974, F1=0.8076, support=304
