# OFF_PTQ_DEEPCONV_LSTM_CONV2D_E12_ARDUINO TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E12_arduino_from_scratch_T50/no_accel_rotation_v2/deepconv_lstm_conv2d/e12/deepconv_lstm_conv2d_T50_Prandom_stratified_E12_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 107.62 KB
- Accuracy: 0.8868
- Macro-F1: 0.8919

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v3_target_clusters_p025/off/deepconv_lstm_conv2d/e12/confusion_off_ptq_deepconv_lstm_conv2d_e12_arduino_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9865, R=0.8280, F1=0.9003, support=529
- Jogging: P=0.9960, R=0.9318, F1=0.9628, support=528
- Upstairs: P=0.6410, R=0.9584, F1=0.7682, support=529
- Downstairs: P=0.8735, R=0.8106, F1=0.8409, support=528
- Sitting: P=0.9962, R=1.0000, F1=0.9981, support=528
- Standing: P=0.9929, R=0.7917, F1=0.8809, support=528
