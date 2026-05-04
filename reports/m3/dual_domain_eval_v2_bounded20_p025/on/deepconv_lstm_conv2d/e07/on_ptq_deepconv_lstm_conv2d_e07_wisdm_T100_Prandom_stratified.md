# ON_PTQ_DEEPCONV_LSTM_CONV2D_E07_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E07_skip_inference_norm_diag/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e07/deepconv_lstm_conv2d_T100_Prandom_stratified_E07_deepconv_lstm_r0_ptq_int8.tflite`
- Model size: 136.92 KB
- Accuracy: 0.9665
- Macro-F1: 0.9288

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/on/deepconv_lstm_conv2d/e07/confusion_on_ptq_deepconv_lstm_conv2d_e07_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9848, R=0.9963, F1=0.9905, support=2723
- Jogging: P=0.9943, R=0.9924, F1=0.9934, support=2109
- Upstairs: P=0.8202, R=0.9562, F1=0.8830, support=730
- Downstairs: P=0.9656, R=0.9080, F1=0.9359, support=587
- Sitting: P=0.9946, R=0.9711, F1=0.9827, support=381
- Standing: P=0.9950, R=0.6513, F1=0.7873, support=304
