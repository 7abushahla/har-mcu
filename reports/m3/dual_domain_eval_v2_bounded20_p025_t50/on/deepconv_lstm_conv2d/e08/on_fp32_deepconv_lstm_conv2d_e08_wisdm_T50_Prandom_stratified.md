# ON_FP32_DEEPCONV_LSTM_CONV2D_E08_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E08_T50_window/accel_rotation_v2_bounded20_p025/deepconv_lstm_conv2d/e08/deepconv_lstm_conv2d_T50_Prandom_stratified_E08_deepconv_lstm_r0_fp32.tflite`
- Model size: 396.43 KB
- Accuracy: 0.9590
- Macro-F1: 0.9174

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval_v2_bounded20_p025_t50/on/deepconv_lstm_conv2d/e08/confusion_on_fp32_deepconv_lstm_conv2d_e08_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9885, R=0.9843, F1=0.9864, support=5482
- Jogging: P=0.9932, R=0.9925, F1=0.9928, support=4250
- Upstairs: P=0.7866, R=0.9422, F1=0.8574, support=1541
- Downstairs: P=0.9383, R=0.9127, F1=0.9253, support=1249
- Sitting: P=0.9897, R=0.9871, F1=0.9884, support=777
- Standing: P=0.9948, R=0.6074, F1=0.7542, support=624
