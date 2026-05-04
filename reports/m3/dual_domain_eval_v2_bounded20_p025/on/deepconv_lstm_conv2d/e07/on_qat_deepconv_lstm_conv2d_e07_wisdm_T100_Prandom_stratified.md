# ON_QAT_DEEPCONV_LSTM_CONV2D_E07_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E07_skip_inference_norm_diag/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e07/deepconv_lstm_conv2d_T100_Prandom_stratified_E07_deepconv_lstm_r0_qat.tflite`
- Model size: 137.34 KB
- Accuracy: 0.9418
- Macro-F1: 0.8948

- Input dtype: `<class 'numpy.int8'>`
- Output dtype: `<class 'numpy.int8'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025/on/deepconv_lstm_conv2d/e07/confusion_on_qat_deepconv_lstm_conv2d_e07_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9830, R=0.9776, F1=0.9803, support=2723
- Jogging: P=0.9985, R=0.9573, F1=0.9775, support=2109
- Upstairs: P=0.7172, R=0.9658, F1=0.8231, support=730
- Downstairs: P=0.9007, R=0.8501, F1=0.8747, support=587
- Sitting: P=0.9919, R=0.9606, F1=0.9760, support=381
- Standing: P=0.9343, R=0.6086, F1=0.7371, support=304
