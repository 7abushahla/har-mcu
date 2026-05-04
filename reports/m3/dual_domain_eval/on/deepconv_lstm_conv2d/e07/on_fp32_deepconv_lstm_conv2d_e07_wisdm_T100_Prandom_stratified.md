# ON_FP32_DEEPCONV_LSTM_CONV2D_E07_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E07_skip_inference_norm_diag/accel_rotation/deepconv_lstm_conv2d/e07/deepconv_lstm_conv2d_T100_Prandom_stratified_E07_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.9495
- Macro-F1: 0.8982

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/deepconv_lstm_conv2d/e07/confusion_on_fp32_deepconv_lstm_conv2d_e07_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9915, R=0.9908, F1=0.9912, support=2723
- Jogging: P=0.9942, R=0.9763, F1=0.9852, support=2109
- Upstairs: P=0.7295, R=0.9644, F1=0.8307, support=730
- Downstairs: P=0.9359, R=0.8961, F1=0.9156, support=587
- Sitting: P=0.9898, R=0.7612, F1=0.8605, support=381
- Standing: P=0.9550, R=0.6974, F1=0.8061, support=304
