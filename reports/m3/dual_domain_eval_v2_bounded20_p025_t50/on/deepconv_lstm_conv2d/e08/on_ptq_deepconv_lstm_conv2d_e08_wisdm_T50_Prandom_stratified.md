# ON_PTQ_DEEPCONV_LSTM_CONV2D_E08_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E08_T50_window/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e08/deepconv_lstm_conv2d_T50_Prandom_stratified_E08_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 107.62 KB
- Accuracy: 0.9592
- Macro-F1: 0.9175

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025_t50/on/deepconv_lstm_conv2d/e08/confusion_on_ptq_deepconv_lstm_conv2d_e08_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9883, R=0.9849, F1=0.9866, support=5482
- Jogging: P=0.9932, R=0.9925, F1=0.9928, support=4250
- Upstairs: P=0.7865, R=0.9442, F1=0.8582, support=1541
- Downstairs: P=0.9413, R=0.9119, F1=0.9264, support=1249
- Sitting: P=0.9897, R=0.9871, F1=0.9884, support=777
- Standing: P=0.9974, R=0.6042, F1=0.7525, support=624
