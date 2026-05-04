# ON_PTQ_DEEPCONV_LSTM_CONV2D_E08_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E08_T50_window/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e08/deepconv_lstm_conv2d_T50_Prandom_stratified_E08_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 107.62 KB
- Accuracy: 0.9486
- Macro-F1: 0.8968

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/on/deepconv_lstm_conv2d/e08/confusion_on_ptq_deepconv_lstm_conv2d_e08_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9816, R=0.9816, F1=0.9816, support=5482
- Jogging: P=0.9915, R=0.9894, F1=0.9905, support=4250
- Upstairs: P=0.7491, R=0.9338, F1=0.8313, support=1541
- Downstairs: P=0.9390, R=0.8631, F1=0.8995, support=1249
- Sitting: P=0.9660, R=0.9871, F1=0.9764, support=777
- Standing: P=1.0000, R=0.5401, F1=0.7014, support=624
