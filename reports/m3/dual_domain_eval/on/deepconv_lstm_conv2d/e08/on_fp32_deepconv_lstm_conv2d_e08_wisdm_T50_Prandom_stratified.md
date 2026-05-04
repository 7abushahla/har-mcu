# ON_FP32_DEEPCONV_LSTM_CONV2D_E08_WISDM TFLite Evaluation (T=50, protocol=random_stratified)

- Model: `/shared/b00088568/github/har-mcu/models_tflite/m3/E08_T50_window/accel_rotation/deepconv_lstm_conv2d/e08/deepconv_lstm_conv2d_T50_Prandom_stratified_E08_deepconv_lstm_r0_fp32.tflite`
- Model size: 396.43 KB
- Accuracy: 0.9629
- Macro-F1: 0.9495

- Input dtype: `<class 'numpy.float32'>`
- Output dtype: `<class 'numpy.float32'>`
- Interpreter op count: 5
- Interpreter ops: `['CONV_2D', 'FULLY_CONNECTED', 'RESHAPE', 'SOFTMAX', 'UNIDIRECTIONAL_SEQUENCE_LSTM']`
- Confusion matrix plot: `reports/m3/dual_domain_eval/on/deepconv_lstm_conv2d/e08/confusion_on_fp32_deepconv_lstm_conv2d_e08_wisdm_T50_Prandom_stratified.png`

## Per-class metrics

- Walking: P=0.9825, R=0.9818, F1=0.9821, support=5482
- Jogging: P=0.9888, R=0.9758, F1=0.9822, support=4250
- Upstairs: P=0.8937, R=0.8890, F1=0.8913, support=1541
- Downstairs: P=0.8632, R=0.9095, F1=0.8858, support=1249
- Sitting: P=0.9746, R=0.9884, F1=0.9815, support=777
- Standing: P=0.9821, R=0.9663, F1=0.9742, support=624
