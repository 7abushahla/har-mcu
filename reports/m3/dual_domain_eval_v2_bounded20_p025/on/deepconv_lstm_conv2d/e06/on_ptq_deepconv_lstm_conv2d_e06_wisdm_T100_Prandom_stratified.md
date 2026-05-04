# ON_PTQ_DEEPCONV_LSTM_CONV2D_E06_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E06_no_norm_matched/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e06/deepconv_lstm_conv2d_T100_Prandom_stratified_E06_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.9639
- Macro-F1: 0.9346

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/on/deepconv_lstm_conv2d/e06/confusion_on_ptq_deepconv_lstm_conv2d_e06_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9900, R=0.9827, F1=0.9864, support=2723
- Jogging: P=0.9981, R=0.9877, F1=0.9929, support=2109
- Upstairs: P=0.7900, R=0.9740, F1=0.8724, support=730
- Downstairs: P=0.9572, R=0.8756, F1=0.9146, support=587
- Sitting: P=0.9974, R=0.9895, F1=0.9934, support=381
- Standing: P=0.9869, R=0.7434, F1=0.8480, support=304
