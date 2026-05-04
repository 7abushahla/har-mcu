# ON_QAT_DEEPCONV_LSTM_CONV2D_E07_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E07_skip_inference_norm_diag/accel_rotation/deepconv_lstm_conv2d/e07/deepconv_lstm_conv2d_T100_Prandom_stratified_E07_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.3854
- Macro-F1: 0.2747

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/deepconv_lstm_conv2d/e07/confusion_on_qat_deepconv_lstm_conv2d_e07_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.6679, R=0.2710, F1=0.3856, support=2723
- Jogging: P=0.9176, R=0.5017, F1=0.6487, support=2109
- Upstairs: P=0.1769, R=0.6027, F1=0.2735, support=730
- Downstairs: P=0.1876, R=0.6644, F1=0.2926, support=587
- Sitting: P=0.6000, R=0.0079, F1=0.0155, support=381
- Standing: P=1.0000, R=0.0164, F1=0.0324, support=304
