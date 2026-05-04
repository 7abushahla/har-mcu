# OFF_FP32_DEEPCONV_LSTM_CONV2D_E07_WISDM TFLite Evaluation (T=100, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E07_skip_inference_norm_diag/no_accel_rotation/deepconv_lstm_conv2d/e07/deepconv_lstm_conv2d_T100_Prandom_stratified_E07_deepconv_lstm_r0_fp32.tflite`
- Model size: 513.62 KB
- Accuracy: 0.9824
- Macro-F1: 0.9719

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/off/deepconv_lstm_conv2d/e07/confusion_off_fp32_deepconv_lstm_conv2d_e07_wisdm_T100_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9923, R=0.9901, F1=0.9912, support=2723
- Jogging: P=0.9962, R=0.9953, F1=0.9957, support=2109
- Upstairs: P=0.9126, R=0.9726, F1=0.9416, support=730
- Downstairs: P=0.9683, R=0.9370, F1=0.9524, support=587
- Sitting: P=0.9895, R=0.9895, F1=0.9895, support=381
- Standing: P=0.9965, R=0.9276, F1=0.9608, support=304
