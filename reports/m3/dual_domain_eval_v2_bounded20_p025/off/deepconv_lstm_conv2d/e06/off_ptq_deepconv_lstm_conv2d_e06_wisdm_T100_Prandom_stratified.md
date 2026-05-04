# OFF_PTQ_DEEPCONV_LSTM_CONV2D_E06_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E06_no_norm_matched/no_accel_rotation_v2/deepconv_lstm_conv2d/e06/deepconv_lstm_conv2d_T100_Prandom_stratified_E06_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.9845
- Macro-F1: 0.9756

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/off/deepconv_lstm_conv2d/e06/confusion_off_ptq_deepconv_lstm_conv2d_e06_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9959, R=0.9930, F1=0.9945, support=2723
- Jogging: P=0.9967, R=0.9938, F1=0.9953, support=2109
- Upstairs: P=0.9417, R=0.9521, F1=0.9469, support=730
- Downstairs: P=0.9377, R=0.9489, F1=0.9433, support=587
- Sitting: P=0.9896, R=0.9948, F1=0.9921, support=381
- Standing: P=0.9867, R=0.9770, F1=0.9818, support=304
